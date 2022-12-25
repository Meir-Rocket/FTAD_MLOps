import ast
import os
import json

from flask import Flask
from flask_restx import Api, Resource, reqparse

from domain.config import load_config
from domain.enums import EModels
from scripts.excel_import import import_data
from scripts.calc import run_calc


app = Flask(__name__)
api = Api(app)


@api.route('/models', endpoint='models', methods=['GET'])
class AvailableModels(Resource):

    @staticmethod
    @api.response(200, 'OK')
    def get():
        return json.dumps(EModels.name_values_dict()), 200


@api.route('/data', endpoint='data', methods=['POST'])
class Data(Resource):
    pass


estimated_models_parser_1 = reqparse.RequestParser()
estimated_models_parser_1.add_argument('model', type=str, help='Model key (for more info check out available models)',
                                       required=True, location='json', choices=list(EModels.name_values_dict().keys()))

estimated_models_parser_2 = reqparse.RequestParser()
estimated_models_parser_2.add_argument('model', type=str, help='Model file name to delete', required=True,
                                       location='json')


@api.route('/estimated_models', endpoint='estimated_models', methods=['GET', 'POST', 'DELETE'])
class EstimatedModels(Resource):
    api: Api
    data_path: str
    estimated_models_path: str
    params_path: str
    storage_path: str

    def __init__(self, appi: Api = api):
        self.api = appi
        if cfg['ESTIMATED_MODELS_PATH']:
            self.estimated_models_path = cfg['ESTIMATED_MODELS_PATH']
        else:
            self.estimated_models_path = os.getcwd() + '/res'

        if cfg['MODEL_PARAMETERS_PATH']:
            self.params_path = cfg['MODEL_PARAMETERS_PATH']
        else:
            self.params_path = os.getcwd() + '/data/parameters'

        if cfg['STORAGE_PATH']:
            self.storage_path = cfg['STORAGE_PATH']
        else:
            self.storage_path = os.getcwd() + '/res/split_storage'
        super().__init__(self.api)

    @api.doc(
        responses={
            200: 'OK'
        })
    def get(self):
        return json.dumps({'Estimated models': os.listdir(self.estimated_models_path)}), 200

    @api.expect(estimated_models_parser_1)
    @api.doc(
        params={
            'model': 'Model key (for more info check out available models)'
        },
        responses={
            200: 'OK'
        })
    def post(self):
        args = estimated_models_parser_1.parse_args()
        with open(self.params_path, 'r') as f:
            params = dict(json.load(f))
        kwargs = {
            'storage_path': self.storage_path,
            'model_id': EModels.get_value_by_name(args['model']),
            'model_params': params
        }
        run_calc(cfg=cfg, mode=1, kwargs=kwargs)
        return 'Model training completed', 200

    @api.expect(estimated_models_parser_2)
    @api.doc(
        params={
            'model': 'Model file name to delete'
        },
        responses={
            204: 'Model successfully deleted.',
            404: 'File not found.'
        })
    def delete(self):
        args = estimated_models_parser_2.parse_args()
        path = self.estimated_models_path + '/' + args['model']
        try:
            os.remove(path)
        except FileNotFoundError:
            return 'Given file not found. Check path and filename and try again.', 404
        return 'Completed', 204


params_parser_1 = reqparse.RequestParser()
params_parser_1.add_argument('model', type=str, help='Model key (for more info check out available models)',
                             required=True, location='json', choices=list(EModels.name_values_dict().keys()))

params_parser_2 = reqparse.RequestParser()
params_parser_2.add_argument('model', type=str, help='Model key (for more info check out available models)',
                             required=True, location='json', choices=list(EModels.name_values_dict().keys()))
params_parser_2.add_argument('model_params', type=str, help='Parameters for model estimation (ONLY FOR PUT)',
                             required=True, location='json', default='{}')


@api.route('/model_parameters', endpoint='model_parameters', methods=['GET', 'PUT'])
class ModelParameters(Resource):
    api: Api
    params_path: str

    def __init__(self, appi: Api = api):
        self.api = appi
        if cfg['MODEL_PARAMETERS_PATH']:
            self.params_path = cfg['MODEL_PARAMETERS_PATH']
        else:
            self.params_path = os.getcwd() + '/data/parameters/'
        super().__init__(self.api)

    @api.expect(params_parser_1)
    @api.doc(
        params={
            'model': 'Model key (for more info check out available models)'
        },
        responses={
            200: 'OK',
            404: 'File not found.'
        })
    def get(self):
        args = params_parser_1.parse_args()
        model = args['model'].replace('_', '').title()
        path = self.params_path + model + '_parameters.json'
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return data, 200
        except FileNotFoundError:
            return 'Given file not found. Check path and model and try again.', 404

    @api.expect(params_parser_2)
    @api.doc(
        params={
            'model': 'Model key (for more info check out available models)',
            'model_params': 'Parameters for model estimation (ONLY FOR PUT)'
        },
        responses={
            200: 'OK',
        })
    def put(self):
        args = params_parser_2.parse_args()
        model = args['model'].replace('_', '').title()
        path = self.params_path + model + '_parameters.json'
        with open(path, 'w') as f:
            params = ast.literal_eval(args['model_params'])
            json_object = json.dumps(params, indent=4)
            f.write(json_object)
            f.close()
        return 'Parameters updated.', 200


if __name__ == '__main__':
    cfg = load_config()
    import_data(cfg)
    app.run(debug=cfg['DEBUG'])

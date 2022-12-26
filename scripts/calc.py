import joblib
import pandas as pd

from typing import Optional

from dbs.database import DatabaseSession
from dbs.entities import Data
from domain.enums import EModels, EModes, DataSheetIndexes
from model.base import Dataset, Model, Pipe, base_estimators


def train(data: pd.DataFrame, storage_path: str, model_id: int, model_params: Optional[dict]):
    dataset = Dataset(data, 'data', 'edu_index', storage_path)
    model = Model(base_estimators[model_id], model_id, EModels(model_id).name, model_params)
    pipe = Pipe(dataset, model)
    pipe.fit()


def predict(model_path: str, prediction_path: str):
    pipe = joblib.load(model_path)
    pipe.predict(prediction_path)


def get_data(cfg: dict):
    with DatabaseSession(cfg['SQLALCHEMY_DATABASE']) as session:
        qr = session.query(
            Data.id,
            Data.edu_index,
            Data.science_index,
            Data.inter_index,
            Data.fin_index,
            Data.wage,
            Data.add,
            Data.exam_1,
            Data.exam_2,
            Data.exam_3,
            Data.avg_exam_1,
            Data.stud_num_1,
            Data.stud_num_2,
            Data.stud_num_3,
            Data.w_1,
            Data.w_2,
            Data.w_3,
            Data.w_4,
            Data.w_5,
            Data.asp_num,
            Data.w_6,
            Data.w_7,
            Data.citation_1,
            Data.citation_2,
            Data.citation_3,
            Data.pub_num_1,
            Data.pub_num_2,
            Data.pub_num_3,
            Data.research_num,
            Data.w_8,
            Data.w_9,
            Data.research_incom,
            Data.license_num,
            Data.w_10,
            Data.w_11,
            Data.w_12,
            Data.journal_num,
            Data.grants_num,
            Data.w_13,
            Data.w_14,
            Data.w_15,
            Data.w_16,
            Data.w_17,
            Data.w_18,
            Data.stud_num_4,
            Data.w_19,
            Data.prof_num,
            Data.w_20,
            Data.w_21,
            Data.money_1,
            Data.money_2,
            Data.income_per_npr,
            Data.w_22,
            Data.avg_wage_1,
            Data.total_income,
            Data.total_square_1,
            Data.square_1,
            Data.square_2,
            Data.square_3,
            Data.square_4,
            Data.computer_number,
            Data.w_23,
            Data.books,
            Data.w_24,
            Data.w_25,
            Data.w_26,
            Data.npr_num,
            Data.w_27,
            Data.total_stud_num_1,
            Data.stud_num_5,
            Data.stud_num_6,
            Data.stud_num_7,
            Data.avg_exam_2,
            Data.w_28,
            Data.w_29,
            Data.w_30,
            Data.stud_num_8,
            Data.stud_num_9,
            Data.company_num_1,
            Data.company_num_2,
            Data.money_3,
            Data.money_4,
            Data.total_pub_num,
            Data.bi_num,
            Data.tp_num,
            Data.ccus_num,
            Data.sb_num,
            Data.total_asp_num,
            Data.w_31,
            Data.total_doc_num,
            Data.diss_sov_num,
            Data.total_work_num,
            Data.total_pps_num,
            Data.total_sci_num,
            Data.w_32,
            Data.w_33,
            Data.w_34,
            Data.w_35,
            Data.avg_wage_2,
            Data.avg_wage_3,
            Data.for_stud_num,
            Data.w_36,
            Data.total_prog_num,
            Data.total_stud_num_2,
            Data.total_for_asp_num,
            Data.citation_4,
            Data.for_income_1,
            Data.for_income_2,
            Data.results_num,
            Data.total_square_2,
            Data.lab_square,
            Data.research_square,
            Data.living_square,
            Data.sport_square,
            Data.w_37,
            Data.comp_num,
            Data.w_38,
            Data.library,
            Data.income,
            Data.non_budget_income,
            Data.w_39,
            Data.w_40,
            Data.w_41,
            Data.w_42,
            Data.w_43,
            Data.w_44,
            Data.w_45
        ).all()
    return pd.DataFrame([[result[i] for i in range(len(qr[0]))] for result in qr],
                        columns=list(DataSheetIndexes.name_values_dict().keys()))


def run_calc(cfg: dict, mode: int = 1, **kwargs):
    assert EModes.has_value(mode), 'CAN NOT UNDERSTAND YOUR QUERY!'
    kwargs = kwargs['kwargs']
    if mode == 1:
        data = get_data(cfg)
        train(data, kwargs['storage_path'], kwargs['model_id'], kwargs['model_params'])
    elif mode == 2:
        predict(kwargs['model_path'], kwargs['prediction_path'])

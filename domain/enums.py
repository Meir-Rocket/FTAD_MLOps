import enum


class AppIntEnum(enum.IntEnum):

    @classmethod
    def get_value_by_name(cls, name: str) -> int:
        return cls.__members__.get(name).value if cls.__members__.get(name, 0) else 0

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def name_values_dict(cls) -> dict:
        return {k.name: k.value for k in cls}


class EErrors(AppIntEnum):
    pass


class EModels(AppIntEnum):
    LASSO_REGRESSION = 1
    LINEAR_REGRESSION = 2
    RIDGE_REGRESSION = 3


class EModes(AppIntEnum):
    TRAIN = 1
    PREDICT = 2
    OTHER = 3


class SheetNames(enum.Enum):
    data = 'data'
    info = 'about'


class DataSheetIndexes(AppIntEnum):
    id = 0
    edu_index = 1
    science_index = 2
    inter_index = 3
    fin_index = 4
    wage = 5
    add = 6
    exam_1 = 7
    exam_2 = 8
    exam_3 = 9
    avg_exam_1 = 10
    stud_num_1 = 11
    stud_num_2 = 12
    stud_num_3 = 13
    w_1 = 14
    w_2 = 15
    w_3 = 16
    w_4 = 17
    w_5 = 18
    asp_num = 19
    w_6 = 20
    w_7 = 21
    citation_1 = 22
    citation_2 = 23
    citation_3 = 24
    pub_num_1 = 25
    pub_num_2 = 26
    pub_num_3 = 27
    research_num = 28
    w_8 = 29
    w_9 = 30
    research_incom = 31
    license_num = 32
    w_10 = 33
    w_11 = 34
    w_12 = 35
    journal_num = 36
    grants_num = 37
    w_13 = 38
    w_14 = 39
    w_15 = 40
    w_16 = 41
    w_17 = 42
    w_18 = 43
    stud_num_4 = 44
    w_19 = 45
    prof_num = 46
    w_20 = 47
    w_21 = 48
    money_1 = 49
    money_2 = 50
    income_per_npr = 51
    w_22 = 52
    avg_wage_1 = 53
    total_income = 54
    total_square_1 = 55
    square_1 = 56
    square_2 = 57
    square_3 = 58
    square_4 = 59
    computer_number = 60
    w_23 = 61
    books = 62
    w_24 = 63
    w_25 = 64
    w_26 = 65
    npr_num = 66
    w_27 = 67
    total_stud_num_1 = 68
    stud_num_5 = 69
    stud_num_6 = 70
    stud_num_7 = 71
    avg_exam_2 = 72
    w_28 = 73
    w_29 = 74
    w_30 = 75
    stud_num_8 = 76
    stud_num_9 = 77
    company_num_1 = 78
    company_num_2 = 79
    money_3 = 80
    money_4 = 81
    total_pub_num = 82
    bi_num = 83
    tp_num = 84
    ccus_num = 85
    sb_num = 86
    total_asp_num = 87
    w_31 = 88
    total_doc_num = 89
    diss_sov_num = 90
    total_work_num = 91
    total_pps_num = 92
    total_sci_num = 93
    w_32 = 94
    w_33 = 95
    w_34 = 96
    w_35 = 97
    avg_wage_2 = 98
    avg_wage_3 = 99
    for_stud_num = 100
    w_36 = 101
    total_prog_num = 102
    total_stud_num_2 = 103
    total_for_asp_num = 104
    citation_4 = 105
    for_income_1 = 106
    for_income_2 = 107
    results_num = 108
    total_square_2 = 109
    lab_square = 110
    research_square = 111
    living_square = 112
    sport_square = 113
    w_37 = 114
    comp_num = 115
    w_38 = 116
    library = 117
    income = 118
    non_budget_income = 119
    w_39 = 120
    w_40 = 121
    w_41 = 122
    w_42 = 123
    w_43 = 124
    w_44 = 125
    w_45 = 126


class InfoSheetIndexes(AppIntEnum):
    id = 0
    var_name = 1
    var_description = 2

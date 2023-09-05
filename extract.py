import pandas as pd


def convert_in2mm(x):
    return x*25.4


def extract_tools(df):
    df_tools = df[df['header'].str.contains('P\d+R')].copy()

    df_tools['Tool'] = df_tools['header'].str.extract(r'P(\d+)R').astype('int')
    df_tools['Category'] = df_tools['header'].str.extract(
        r'(L\d+)P').astype('str')
    df_tools['Value'] = df_tools['header'].str.extract(
        r"P\d+R(-?[0-9]\d*\.\d+)").astype('float').apply(convert_in2mm)

    cat_dict = {
        "L10": "Tool Length Geo",
        "L11": "Tool Length Wear",
        "L12": "Tool Radius Geo",
        "L13": "Tool Radius Wear",
    }

    df_tools['Category'] = df_tools['Category'].map(cat_dict)

    df_tools_pivot = df_tools.pivot_table(
        index="Tool", columns="Category", values="Value")

    return df_tools_pivot


def extract_offsets(df):
    df_works = df[df['header'].str.contains('P\d+X')].copy()

    df_works['Tool'] = df_works['header'].str.extract(r'P(\d+)X').astype('int')
    df_works['Category'] = df_works['header'].str.extract(
        r'(L\d+)P').astype('str')
    df_works['Tool-Cat'] = df_works['Tool'].astype(
        'str') + "-" + df_works['Category']
    df_works['X_Value'] = df_works['header'].str.extract(
        r"X(-?[0-9]\d*\.\d+)").astype('float').apply(convert_in2mm)
    df_works['Y_Value'] = df_works['header'].str.extract(
        r"Y(-?[0-9]\d*\.\d+)").astype('float').apply(convert_in2mm)
    df_works['Z_Value'] = df_works['header'].str.extract(
        r"Z(-?[0-9]\d*\.\d+)").astype('float').apply(convert_in2mm)
    df_works['W_Value'] = df_works['header'].str.extract(
        r"W(-?[0-9]\d*\.\d+)").astype('float')
    df_works['A_Value'] = df_works['header'].str.extract(
        r"A(-?[0-9]\d*\.\d+)").astype('float')

    coord_dict = {
        "0-L2": "COMMON",
        "1-L2": "G54",
        "2-L2": "G55",
        "3-L2": "G56",
        "4-L2": "G57",
        "1-L20": "G54.1P1",
        "2-L20": "G54.1P2",
        "3-L20": "G54.1P3",
        "4-L20": "G54.1P4"
    }

    df_works['Coord'] = df_works["Tool-Cat"].map(coord_dict)

    df_works_pivot = df_works[['Coord', 'X_Value', 'Y_Value',
                               'Z_Value', 'W_Value', 'A_Value']].dropna(subset='Coord')
    df_works_pivot = df_works_pivot.set_index('Coord')

    return df_works_pivot


def extract_CMM(df):
    df_ = df.copy()[['Characteristic', 'K1 Measured value', 'K80 Sample', 'K7 Nest', 'K4 Time/Date',
                     'K2101 Nominal value', 'K2110 Lower limit', 'K2111 Upper limit', 'K2142 Unit']]
    df_ = df_.astype({'Characteristic': 'str',
                      'K1 Measured value': 'float64',
                      'K80 Sample': 'str',
                      'K7 Nest': 'str',
                      'K4 Time/Date': 'datetime64[ns]',
                      'K2101 Nominal value': 'float64',
                      'K2110 Lower limit': 'float64',
                      'K2111 Upper limit': 'float64',
                      'K2142 Unit': 'str'})
    df_pivot = df_.pivot_table(index=['K80 Sample', 'K7 Nest', 'K4 Time/Date'],
                               columns='Characteristic', values='K1 Measured value')
    df_pivot = df_pivot.reset_index()
    df_pivot = df_pivot.sort_values(by="K4 Time/Date", ascending=True)
    df_pivot = df_pivot.drop_duplicates(
        subset=['K80 Sample', 'K7 Nest'], keep='last')
    df_pivot = df_pivot[['K80 Sample', 'K7 Nest', 'K4 Time/Date',
                        'Q1 - Top Profile^Max', 'Q1 - Top Profile^Min',
                         'Q2 - Top Parallelism',
                         'Q3 - Left Tab Profile^Max', 'Q3 - Left Tab Profile^Min', 'Q3 - Right Tab Profile^Max', 'Q3 - Right Tab Profile^Min',
                         'Q4 - Top Width_X',
                         'Q5 - Top Position', 'Q5 - Top Position.X',
                         'Long Axis Position', 'Long Axis Position.Y', 'Long Axis Width_Y']]
    return df_pivot

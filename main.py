import pandas as pd
import matplotlib.pyplot as plt

# Constraints
IGNORED_COUNTRIES = ['EA', 'EU27_2007', 'EU27_2020', 'EU28']
FIRST_COL_CONSTRAINT_1 = "BEDPL,NR,I551,"
FIRST_COL_CONSTRAINT_2 = "IND_TOTAL"

# Output file columns
OUTPUT_DATA_COLUMNS = ['Country Code', 'Percentage of individuals online', 'Number of Bed-places']


def get_cleaned_df(file_path, constraint) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep='\s*\t\s*')
    columns = list(df.columns)
    df_new = df.loc[
        (df[columns[0]].str.contains(constraint))
        & ~(df[columns[0]].str.contains(IGNORED_COUNTRIES[0]))
        & ~(df[columns[0]].str.contains(IGNORED_COUNTRIES[1]))
        & ~(df[columns[0]].str.contains(IGNORED_COUNTRIES[2]))
        & ~(df[columns[0]].str.contains(IGNORED_COUNTRIES[3]))
        ]
    df_new = df_new[[columns[0], '2016']]
    return df_new


def validate_value(value):
    if value[-1] == 'b':
        value = value[:-2]
    elif 'u' in value:
        value = ':'
    return value


def process_df(df, first_stage_process=False):
    for index, row in df.iterrows():
        country = row[0].split(',')[3]
        value = validate_value(row[1])
        if not result_data.get(country):
            if first_stage_process:
                result_data[country] = [value, ':']
            else:
                result_data[country] = [':', value]
        else:
            result_data[country][1] = value


def save_bar_charts(data):
    data[OUTPUT_DATA_COLUMNS[1]] = [0 if i == ':' else int(i) for i in data[OUTPUT_DATA_COLUMNS[1]]]
    data[OUTPUT_DATA_COLUMNS[2]] = [0 if i == ':' else int(i) for i in data[OUTPUT_DATA_COLUMNS[2]]]
    plt.figure(figsize=(15, 12), dpi=150)
    plt.subplot(2, 1, 1)
    plt.bar(data[OUTPUT_DATA_COLUMNS[0]], data[OUTPUT_DATA_COLUMNS[1]])
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.ylabel('Individuals online', fontweight="bold")
    plt.title('Percentage of individuals online and Num. of bed places Vs Country Codes', fontweight="bold")

    plt.subplot(2, 1, 2)
    plt.bar(data[OUTPUT_DATA_COLUMNS[0]], data[OUTPUT_DATA_COLUMNS[2]])
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.xlabel('Country', fontweight="bold")
    plt.ylabel('Bed places', fontweight="bold")

    plt.savefig('output_files/bar_chart.png')


def save_table(data):
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(1, 1)
    ax.axis('off')
    tab = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc='left', colWidths=[0.2, 0.4, 0.4], bbox=[0, 0, 1, 1])
    for i in range(len(df.columns)):
        tab[(0, i)].set_facecolor("cyan")

    plt.savefig('output_files/table.png')


def save_csv(data):
    df_final = pd.DataFrame(data)
    df_final.to_csv("output_files/out_data.csv", index=False)


result_data = {}
if __name__ == '__main__':

    df1 = get_cleaned_df("data/tour_cap_nat.tsv", FIRST_COL_CONSTRAINT_1)
    process_df(df1, first_stage_process=True)
    df2 = get_cleaned_df("data/tin00083.tsv", FIRST_COL_CONSTRAINT_2)
    process_df(df2, first_stage_process=False)
    data_final = {
        OUTPUT_DATA_COLUMNS[0]: [],
        OUTPUT_DATA_COLUMNS[1]: [],
        OUTPUT_DATA_COLUMNS[2]: []
    }
    for d in result_data:
        data_final[OUTPUT_DATA_COLUMNS[0]].append(d)
        data_final[OUTPUT_DATA_COLUMNS[1]].append(result_data[d][1])
        data_final[OUTPUT_DATA_COLUMNS[2]].append(result_data[d][0])

    save_csv(data_final)
    save_table(data_final)
    save_bar_charts(data_final)

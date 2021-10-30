from bs4 import BeautifulSoup
import pandas as pd
import os


def get_table_arr(filename):
    with open(filename, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    table_arr = []
    for tr in soup.table.find_all('tr'):
        divs = tr.div.contents
        table_arr.append([divs[0].get_text(), divs[1].get_text(), divs[2].get_text(), divs[3].get_text().strip(),
                          divs[6].get_text().replace(",", "").replace("$", ""), divs[7].get_text().replace(",", "")])
    return table_arr


if __name__ == '__main__':
    folder_name = input("Please input the folder name: ")
    file_names = []
    for root, dirs, files in os.walk(folder_name, topdown=False):
        for name in files:
            file_names.append(os.path.join(root, name))
    table_arr = []
    for file_name in file_names:
        table_arr.extend(get_table_arr(file_name))
    table_header = "Date,Card,Status,Description,Amount,Points"
    df = pd.DataFrame(table_arr, columns=table_header.split(','))
    df['Amount'] = pd.to_numeric(df['Amount'])
    df['Points'] = pd.to_numeric(df['Points'])
    points = df.groupby('Description')['Points'].sum()
    dates = df.groupby('Description')['Date'].apply(lambda x: "%s" % ', '.join(x))

    result = pd.concat({"Points": points, "Date": dates}).unstack().T
    result.to_csv(f"{folder_name}.csv")

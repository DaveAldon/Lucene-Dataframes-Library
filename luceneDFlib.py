#DaveAldon Lucene Dataframes Library
import pandas as pd

#Just an example for how to use the functions
def example_function():
    report_name = "Name of Report"
    duplicates = False
    format_title = False
    df = pd.DataFrame(index=index, columns=columns)
    param_list = ['some parameter', 'another parameter']

    #Lucene query builder usage
    query = '()%s' % (param_builder('FIELD_NAME', param_list))
    #CSV maker usage
    output = create_full_csv(report_name, df, duplicates, format_title)

#Builds a Lucene query formatted string of fields from a list
def param_builder(field, params):
    param_str = ''
    for val in params[:-1]:
        param_str += (field + ':("%s") OR ' % val)
    param_str += (field + ':("%s") ' % params[-1])
    return param_str

#TODO Create optional arguments for duplicates and format_title
#Currently you must change some names in here to work properly
def create_full_csv(report_name, df, duplicates, format_title):

    if format_title == True:
        #Initialize a dictionary that will be used to make column names readable
        fields = {}

        #Replaces common values with readable chars, and adds them to the set. title() capitalizes each word
        for column in df:
            fields[column] = column.replace('EXTRA_WORDS_TO_REMOVE', '').replace('_', ' ').title()

        #New csv set that will hold the dataframe's data
        csv_data = []

    if duplicates == True:
        df = df.drop_duplicates(['DUPLICATE_NAME'])

    #Changes column names to their new mapped values in the dictionary
    df = df.rename(columns=fields).fillna("")

    #Below adds the column names and row values to the csv object
    rcount = 1
    csv_data.append(list(""))
    csv_data[0].append(str(','.join(df.columns.values)))
    for index, row in df.iterrows():
        csv_data.append(list(""))
        for column in df:
            csv_data[rcount].append(str(row[column]))
        rcount += 1
    csv_data = map(','.join, csv_data)

    #Output data to whatever means necessary
    return (save_report("%s.csv" % (report_name), "\n".join(csv_data)))

#Gives proper formatting to document you're saving
def save_report(file_name, file_contents, file_mode = 'w+'):
    with artifacts.open(file_name, file_mode) as f:
        f.write(file_contents)
    return artifacts.getURL('/PATH/%s' % file_name)

def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))

    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)
    print(res)

example_function()

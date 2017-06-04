#DaveAldon Lucene Dataframes Library: SQL to URL & Lucene syntax
import requests

#TODO Add more support for lists to be used in main() example, and also make functions more generic so
#that nothing in this module needs to be changed.
def main():
    SELECT = 'Fields to retrieve'
    FROM = 'Database location'
    WHERE = ['Boolean conditions']
    extras = ['Bonus conditions']
    report_name = 'Report Name'
    report_format = 'csv'
    query = ''
    limit = 10

    #Tries the URL method, if it fails then goes full Lucene syntax
    try:
        #Am I trapped in a VM?
        page = requests.get('http://127.0.0.1')
        #I guess not
        query = getQueryURL(SELECT, FROM, WHERE, extras, report_name, report_format)
        page = requests.get(query)
        value = html.fromstring(page.content)
    except:
        print('This instance is trapped!')
        query = getQueryLucene(WHERE) + SELECT + FROM + limit

    print(query)

    #Use the result of query on your database. That's it!

#Pure Lucene converter
def getQueryLucene(WHERE_boolean):
    where = '()'
    for value in WHERE_boolean:
        list_value = value.split('=')
        where += '(%s:("%s"))' % (list_value[0], list_value[1])
    return where

#URL converter
def getQueryURL(SELECT_fields, FROM_store, WHERE_boolean, extra_params, name, format):
    def make_where(values):
        where = '()'
        for value in values:
            #Turns your filthy bool into a URL readable format
            val = value.split('=')
            where += '(%s):%s' % (val[0], val[1].replace(' ', '%'))
        return where

    ip = 'Database address'
    query_type = 'q' #Or whatever you need
    where_clause = make_where(WHERE_boolean)
    select_clause = 'Field_Column_Name=%s' % SELECT_fields
    from_clause = 'Database_Location_Name=%s' % FROM_store
    extra_clause = ''
    name_clause = 'output_file_path=%s' % name
    format_clause = 'format=%s' % format

    for val in extra_params:
        extra_clause += val + '&'

    return 'https://%s/search?%s=%s&%s&%s&%s&%s' % (ip, query_type, where_clause, select_clause, extra_clause, name_clause, format_clause)

main()

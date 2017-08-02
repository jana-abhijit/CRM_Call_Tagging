import MySQLdb
from BeautifulSoup import BeautifulSoup
import datetime
from charts import generate_pie_chart, generate_bar_chart


def get_all_filenames():

    with open("config.xml") as f:
        content = f.read()

    y = BeautifulSoup(content)
    host_name = y.mysql.host.contents[0]
    user_name = y.mysql.user.contents[0]
    password = y.mysql.passwd.contents[0]

    directory = y.others.dir.contents[0]

    db = MySQLdb.connect(host_name,user_name,password)

    cursor = db.cursor()

    sql_1 = '''select a.tag_id, count(a.tag_id), b.level1, b.level2, b.level3
    from agrostar_crm.order_management_calltagmapping a
    join agrostar_crm.order_management_tag b
    on a.tag_id = b.id
    join agrostar_crm.csr_billingaddress c
    on c.id = a.farmer_id
    where date(a.created_on) >= date_sub(curdate(),interval 8 day)
    and c.state like %s
    group by a.tag_id'''

    sql_2 = '''select product, count(product) from agrostar_crm.order_management_calltagmapping b
    join agrostar_crm.csr_billingaddress c
    on c.id = b.farmer_id
    where b.tag_id in (select a.id from agrostar_crm.order_management_tag a
        where a.level1 like '%%product inquires%%'
        and a.level2 like '%%product search%%')
    and date(b.created_on) >= date_sub(curdate(),interval 8 day)
    and c.state like %s
    group by product
    order by count(product) desc
    limit 5'''

    sql_3 = '''select distinct level1 from agrostar_crm.order_management_tag;
    '''

    states = ['Maharashtra', 'Gujarat', 'Rajasthan']

    cursor.execute(sql_3)
    results_3 = cursor.fetchall()
    level_one_tags = []
    for row in results_3:
        level_one_tags += [row[0]]

    level_one_tags = list(set(level_one_tags))
    bar_filenames_statewise_dict = {}

    for level_one_tag in level_one_tags:
        bar_filenames_statewise_dict[level_one_tag] = {'Maharashtra':'', 'Gujarat':'', 'Rajasthan':''}

    #Tag Level 1 and 2
    pie_filenames_statewise = []
    ps_filenames_statewise = []
    for state in states:
        cursor.execute(sql_1, ('%%%s%%' % state,))
        results_1 = cursor.fetchall()
        level_one = []
        for row in results_1:
            level_one += [row[2]]

        #Product Inquires - Product Search
        cursor.execute(sql_2, ('%%%s%%' % state,))
        results_2 = cursor.fetchall()
        product_inquires = []
        product_inquires_count = []
        for row in results_2:
            product_inquires += [row[0]]
            product_inquires_count += [row[1]]

        curdate = datetime.datetime.now()
        curdate = ("%s-%s-%s" % (curdate.year, curdate.month, curdate.day))

        #Tag Level 1
        tag_lvl_one = list(set(level_one))
        tag_lvl_one_dict = {}
        for i in tag_lvl_one:
            tag_lvl_one_dict[i] = 0

        for row in results_1:
            tag_lvl_one_dict[row[2]] += int(row[1])

        tag_lvl_one_count = []
        for i in tag_lvl_one:
            tag_lvl_one_count += [tag_lvl_one_dict[i]]

        #Tag Level 1 Pie Chart Creation
        title = 'Tag Level 1-Percentage of Calls-'+state
        pie_filename = 'tag_level_one_pie'+state+curdate+'.png'
        pie_path = directory + pie_filename
        pie_filenames_statewise += [pie_filename]
        generate_pie_chart(tag_lvl_one, tag_lvl_one_count, title,pie_path)

        #Tag Level 2
        bar_filenames = []
        for level_one_tag in tag_lvl_one:
            level_two = []
            for row in results_1:
                if row[2] == level_one_tag and row[3] != '':
                    level_two += [row[3]]

            tag_lvl_two = list(set(level_two))

            if len(tag_lvl_two) < 2:
                continue

            tag_lvl_two_dict = {}
            for i in tag_lvl_two:
                tag_lvl_two_dict[i] = 0

            for row in results_1:
                if row[2] == level_one_tag:
                    tag_lvl_two_dict[row[3]] += int(row[1])

            tag_lvl_two_count = []
            for i in tag_lvl_two:
                tag_lvl_two_count += [tag_lvl_two_dict[i]]

            tag_lvl_two_zip = zip(tag_lvl_two_count, tag_lvl_two)
            tag_lvl_two_zip = sorted(tag_lvl_two_zip, reverse=True)

            if len(tag_lvl_two_zip) > 5:
                new_tag_lvl_two_zip = []
                for i in range(0, 5):
                    new_tag_lvl_two_zip += [(tag_lvl_two_zip[i])]
                key = 'Others'
                value = 0
                for i in range(5,len(tag_lvl_two_zip)):
                    value += tag_lvl_two_zip[i][0]
                new_tag_lvl_two_zip += [(value, key)]
                tag_lvl_two_zip = new_tag_lvl_two_zip

            tag_lvl_two_zip = filter(lambda x: x[0] > 0, tag_lvl_two_zip)
            tag_lvl_two_unzip = zip(*tag_lvl_two_zip)
            tag_lvl_two_count = list(tag_lvl_two_unzip[0])
            tag_lvl_two = list(tag_lvl_two_unzip[1])

            #Tag Level 2 Bar Chart Creation
            title = 'Tag Level 2-' + level_one_tag + '-' + state
            bar_filename = 'tag_level_two_bar' + '_'.join(level_one_tag.split()) + state +curdate + '.png'
            bar_path = directory + bar_filename
            generate_bar_chart(tag_lvl_two, tag_lvl_two_count, title, bar_path)
            bar_filenames += [bar_filename]

            bar_filenames_statewise_dict[level_one_tag][state] = bar_filename

        #Product Inquires Bar Chart Creation
        title = 'Product Inquires-Product Search-'+state
        ps_bar_filename = 'product_inquires_ps' + state + curdate + '.png'
        ps_bar_path = directory + ps_bar_filename
        generate_bar_chart(product_inquires, product_inquires_count, title, ps_bar_path)

        ps_filenames_statewise += [ps_bar_filename]

    db.close()

    return states, pie_filenames_statewise, bar_filenames_statewise_dict, ps_filenames_statewise

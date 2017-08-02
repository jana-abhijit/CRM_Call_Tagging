from agroutils.mail import send
import MySQLdb
from generate_charts import get_all_filenames
from BeautifulSoup import BeautifulSoup


def send_crm_call_tagging_report(recipients,part2):
    to_param = recipients
    subject_param = 'CRM Call Tagging Report'
    send('',content_html=part2, subject=subject_param, to=to_param)

if __name__ == "__main__":

    #recipients = ['<shardul.sheth@agrostar.in>', '<sitanshu.sheth@agrostar.in>', '<ritesh.alladwar@agrostar.in>', '<mehul.mewada@agrostar.in>', '<rignesh.patel@agrostar.in>', '<ashwini.nagulwar@agrostar.in>', '<Pearl.chitranshi@agrostar.in>', '<nithya.krishnan@agrostar.in>', '<praneeth.kumar@agrostar.in>', '<siddhaarth.iyer@agrostar.in>', '<sidharth.dawre@agrostar.in>', '<jignesh.joshi@agrostar.in>', '<hiren.patel@agrostar.in>', '<pradip.rathod@agrostar.in>', '<chinmoy.banerji@agrostar.in>', '<saneeth@agrostar.in>', '<procurement@agrostar.in>', '<priyanka.kote@agrostar.in>', '<mihir.gajjar@agrostar.in>','<abhijit.jana@agrostar.in>']
    recipients = ['<abhijit.jana@agrostar.in>']

    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="as2d2p",
                         db="analytics",
                         local_infile = 1)

    (states, pie_filenames_statewise, bar_filenames_statewise_dict, ps_filenames_statewise) = get_all_filenames()

    with open("config.xml") as f:
        content = f.read()

    y = BeautifulSoup(content)
    imagelink = y.others.imagelink.contents[0]

    part1='''
<html>
<body>
<table>
'''
    pie_part = "<tr>"
    for pfs in range(0,len(pie_filenames_statewise)):
        pie_part += "<td><img src='" + imagelink + pie_filenames_statewise[pfs] + "' width='420' height='441'></td>"
    pie_part += "</tr>"

    ps_part = "<tr>"
    for pfs in range(0,len(ps_filenames_statewise)):
        ps_part += "<td><img src='" + imagelink + ps_filenames_statewise[pfs] + "' width='420' height='314'></td>"
    ps_part += "</tr>"

    bar_part = ""
    for bfsd in bar_filenames_statewise_dict:
        bfs = bar_filenames_statewise_dict[bfsd]
        flag = 0
        for bar_filename in bfs:
            if bfs[bar_filename] != '':
                flag = 1
        if flag != 0:
            bar_part += "<tr>"
            for state in states:
                if bfs[state] != '':
                    bar_part += "<td><img src='" + imagelink + bfs[state] + "' width='420' height='314'></td>"
                else:
                    bar_part += "<td></td>"
            bar_part += "</tr>"

    part2 = pie_part + bar_part + ps_part

    part3='''
</table>
</body>
</html>'''

    send_crm_call_tagging_report(recipients,part1+part2+part3)

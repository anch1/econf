from typing import Any, Union
from datetime import datetime, date, time
import psycopg2
from flask import Flask, request, render_template, session, redirect, Markup

from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOSTDATABASE'] = "localhost"
app.config['USERNAME'] = "pi"
app.config['PASSWORD'] = "tom321jerry"
app.config['DBNAME'] = "conf"
app.config['CONNECT'] = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                                         password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
app.secret_key = 'hrenpenten'
app.version = '0.0.0.1'

app.enter_enabled = True
app.userlistpage = 0
app.lenthuserlistpage = 3


def refresh_menu():
    if (app.enter_enabled):
        session['enter_enabled'] = True
    else:
        session['enter_enabled'] = False


@app.route('/')
def mainwindow():
    session['pwdminlenth'] = 6
    session['usrr'] = session.get('usrr', '00000000000000000000000000')
    session['is_auth'] = session.get('is_auth', False)
    return render_template('BasePage.html')


@app.route('/registration/')
def registry():
    session['res_reg'] = False
    session['errorstr'] = ""
    session['nm'] = ""
    session['fml'] = ""
    session['sn'] = ""
    session['adr'] = ""
    session['comp_nm'] = ""
    session['uzv'] = ""
    session['em'] = ""
    session['dlgn'] = ""
    session['bd'] = ""
    session['sex'] = ""
    session['ph'] = ""
    session['add_info'] = ""
    session['lgn'] = ""
    session['pwd'] = ""
    session['id_member'] = "-1"

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()
    cursor.execute("select id_dict,name from dict where dict_name='орг' order by name")
    session['res_org'] = cursor.fetchall()

    cursor.execute("select id_dict,name from dict where dict_name='долж' order by name")
    session['dolgns'] = cursor.fetchall()

    cursor.execute("select id_dict,name from dict where dict_name='учзв' order by name")
    session['uzvs'] = cursor.fetchall()

    conn.close()
    return render_template('Registry.html', ver=app.version)


@app.route('/registration/', methods=['POST'])
def write_registry():
    # проеряем что нет такого логина и фио
    session['pwdminlenth'] = 6
    session['res_reg'] = True
    session['errorstr'] = ""
    session['nm'] = request.form['nm']
    session['fml'] = request.form['fml']
    session['sn'] = request.form['sn']
    session['adr'] = request.form['adr']
    session['comp_nm'] = request.form['comp_nm']
    session['uzv'] = request.form['uzv']
    session['em'] = request.form['em']
    session['dlgn'] = request.form['dlgn']
    session['bd'] = request.form['bd']
    session['sex'] = request.form['sex']
    session['ph'] = request.form['ph']
    session['add_info'] = request.form['add_info']
    session['lgn'] = request.form['lgn']
    session['pwd'] = request.form['pwd']
    session['id_member'] = request.form['id_member']

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()
    cursor.execute(" select count(*) from members where login=%s and id_member<>%s",
                   (request.form['lgn'], request.form['id_member'],))

    res = cursor.fetchall()
    if (res[0][0] > 0):
        session['res_reg'] = False
        session['errorstr'] = "Внимание! Такой логин уже зарегистрирован Измените логин и попробуйте еще раз."
    else:
        cursor.execute("select count(*) from members where name=%s and surname=%s and famely=%s and id_member<>%s",
                       (session['nm'], session['fml'], session['sn'], session['id_member'],))
        res = cursor.fetchall()
        if (res[0][0] > 0):
            session['res_reg'] = False
            session[
                'errorstr'] = "Внимание!Пользователь с такими фамилией именем и отчеством уже зарегистрирован. Регистрация не выполнена!"

    if (session['res_reg']):
        if (session['id_member'] == "-1"):
            #                                     1      2       3         4           5         6          7         8            9         10   11        12     13    14      15
            cursor.execute(
                "insert into members(name, surname, famely, id_company, id_acdegree, email, id_position, birsday, id_acposition, sex, phone, add_info, login, pwd, addres) " +
                "values (%s,   %s,      %s,      %s,          %s,        %s,     %s,          %s,        %s,          %s,  %s,     %s,       %s,  %s,   %s) returning id_member;",
                (request.form['nm'], request.form['sn'], request.form['fml'], request.form['comp_nm'],
                 request.form['uzv'], request.form['em'], request.form['dlgn'], request.form['bd'], '0',
                 request.form['sex'], request.form['ph'],
                 request.form['add_info'], request.form['lgn'], request.form['pwd'], request.form['adr'],))
            #                                             1                2                     3                     4                     5                 6                      7                  8             9      10                  11                   12                     13                        14           15
            conn.commit()
            res = cursor.fetchall()
            session['pwdminlenth'] = 6
            session['id_member'] = res[0][0]
            session['errorstr'] = 'Регистрация успешна!'
            session['is_auth'] = True
            app.enter_enabled = False
            refresh_menu()
            conn.close()
            return render_template('welcome.html', ver=app.version)
        else:
            # это редактирование своего профиля
            cursor.execute(
                "update members set name=%s, surname=%s,        famely=%s,           id_company=%s,           id_acdegree=%s,       email=%s,         id_position=%s,        birsday=%s,  id_acposition=%s, sex=%s,              phone=%s,           add_info=%s,              login=%s,             pwd=%s,              addres=%s where id_member=%s",
                (
                    request.form['nm'], request.form['sn'], request.form['fml'], request.form['comp_nm'],
                    request.form['uzv'], request.form['em'], request.form['dlgn'], request.form['bd'], '0',
                    request.form['sex'], request.form['ph'], request.form['add_info'],
                    request.form['lgn'], request.form['pwd'], request.form['adr'], request.form['id_member'],))
            conn.commit()
            conn.close()
            return render_template('Registry.html', ver=app.version)
    else:
        conn.close()
        return render_template('Registry.html', ver=app.version)


@app.route('/login/')
def login():
    session['usrr'] = '00000000000000000000000000'
    return render_template('loginfrm.html', ver=app.version)


@app.route('/login/', methods=['POST'])
def res_login():
    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()
    #               0        1      2        3       4       5      6     7       8         9         10              11            12          13        14
    cursor.execute(
        "select id_member, name, surname, famely, birsday, email, sex, phone, add_info, id_company, id_acdegree, id_position, id_acposition, addres, userright from members where login=%s and pwd=%s",
        (request.form['lgn'], request.form['pwd']))
    res = cursor.fetchall()
    if len(res) <= 0:
        session['pwdminlenth'] = 6
        session['is_auth'] = False
        session['errorlogon'] = 'Ошибка входа - нет такого пользователя или неверен пароль!'
        session['login'] = request.form['lgn']
        conn.close()
        return render_template('loginfrm.html', ver=app.version)
    else:
        app.enter_enabled = False
        refresh_menu()
        session['pwdminlenth'] = 6
        session['is_auth'] = True
        session['id_member'] = res[0][0]
        session['nm'] = res[0][1]
        session['sn'] = res[0][2]
        session['fml'] = res[0][3]
        session['adr'] = res[0][13]
        session['comp_nm'] = res[0][9]
        session['uzv'] = res[0][10]
        session['em'] = res[0][5]
        session['dlgn'] = res[0][11]
        dt = res[0][4]
        s = str(dt.year) + '-' + str(dt.month).rjust(2, '0') + '-' + str(dt.day).rjust(2, '0')
        session['bd'] = s
        session['sex'] = res[0][6]
        session['ph'] = res[0][7]
        session['add_info'] = res[0][8]
        session['usrr'] = res[0][14]
        session['lgn'] = request.form['lgn']
        session['pwd'] = request.form['pwd']
        conn.close()
        return render_template('welcome.html', ver=app.version)


@app.route('/logout/')
def logout():
    session['usrr'] = '00000000000000000000000000'
    session['is_auth'] = False
    no = session.get('nm', '') + ' ' + session.get('sn', '')
    session['res_reg'] = False
    session['errorstr'] = ""
    session['nm'] = ""
    session['fml'] = ""
    session['sn'] = ""
    session['adr'] = ""
    session['comp_nm'] = ""
    session['uzv'] = ""
    session['em'] = ""
    session['dlgn'] = ""
    session['bd'] = ""
    session['sex'] = ""
    session['ph'] = ""
    session['add_info'] = ""
    session['lgn'] = ""
    session['pwd'] = ""
    app.enter_enabled = True
    refresh_menu()
    return render_template('logout.html', ver=app.version, name_out=no)


@app.route('/userlist/<int:nompage>', methods=['GET', 'POST'])
def userlist(nompage):
    au = session.get('is_auth', False)  # type: Union[bool, Any]
    if (not au):
        return redirect("/login/")
    if session['usrr'][0]!='1':
        return redirect("/")

    session['userlist_nompage'] = nompage
    #                    0          1       2        3       4        5       6                 7                 8                       9       10
    sqlstr = "select id_member, m.name, surname, famely, birsday, email, phone, comp.name compname, pos.name posname, acdegr.name  acdegrname, coalesce(addres,' ') " + \
             "from members m left outer join dict comp on (comp.dict_name='орг' and comp.id_dict=m.id_company) " + \
             "left outer join dict pos on (pos.dict_name='долж' and pos.id_dict=m.id_position) " + \
             "left outer join dict acpos on (pos.dict_name='учдолж' and pos.id_dict=m.id_acposition) " + \
             "left outer join dict acdegr on (acdegr.dict_name='учзв' and acdegr.id_dict=m.id_acdegree) " + \
             "where (deleted<>'Д' or deleted is null) " + \
             "order by famely limit " + \
             str(app.lenthuserlistpage) + " offset " + str((nompage - 1) * app.lenthuserlistpage)

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()
    cursor.execute(sqlstr)
    session.userlist = cursor.fetchall()

    cursor.execute("select count(*) from members where (deleted<>'Д' or deleted is null)")
    amountrec = cursor.fetchall()[0][0]
    maxpage = (amountrec // app.lenthuserlistpage) + 1
    userlist_minpage = nompage - 5

    if userlist_minpage < 1:
        userlist_minpage = 1

    userlist_maxpage = nompage + 5
    if userlist_maxpage > maxpage:
        userlist_maxpage = maxpage

    session['nmuserpages'] = []
    session['maxuserpages'] = userlist_maxpage
    for i in range(userlist_minpage, userlist_maxpage + 1):
        session['nmuserpages'].append(i)

    conn.close()
    return render_template('userlist.html', ver=app.version)


@app.route('/edit_user/<int:id_member>')
def edituser(id_member):
    return render_template('Edit_user.html', ver=app.version)


@app.route('/delete_user/<int:id_member>')
def deleteuser(id_member):
    # Сразу создадим соединение и передадим в функцию.
    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])


@app.route('/zlist/<int:nompage>')
def zlist(nompage):
    au = session.get('is_auth', False)
    if (not au):
        return redirect("/login/")
    session['zlist_nompage'] = nompage

    # ***********************
    #                       0             1        2                3                 4       5          6                              7                             8
    sqlstr = "select id_application, theme, comp.name company, sc.name scname, to_char(datefrom, 'dd.mm.yyyy'), to_char(dateto,'dd.mm.yyyy'), statusapplication, m.name||' '||m.surname||' '||m.famely usr, to_char(dateatticle,'dd.mm.yyyy')  " + \
             "from application a left outer join dict comp on (comp.dict_name='орг' and comp.id_dict=a.id_company) " + \
             "left outer join dict sc on (sc.dict_name='онаук' and sc.id_dict=a.id_sciency), members m " + \
             "where (a.deleted<>'Д' or a.deleted is null) and m.id_member=a.id_member " + \
             "order by datefrom, theme limit " + \
             str(app.lenthuserlistpage) + " offset " + str((session['zlist_nompage'] - 1) * app.lenthuserlistpage)

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()

    cursor.execute(sqlstr)

    session.zlist = cursor.fetchall()

    cursor.execute("select count(*) from application where (deleted<>'Д' or deleted is null)")
    amountrec = cursor.fetchall()[0][0]

    maxpage = (amountrec // app.lenthuserlistpage) + 1

    zlist_minpage = nompage - 5
    if (zlist_minpage < 1):
        zlist_minpage = 1

    zlist_maxpage = nompage + 5
    if (zlist_maxpage > maxpage):
        zlist_maxpage = maxpage

    session['nmzpages'] = []
    session['maxzpages'] = zlist_maxpage
    for i in range(zlist_minpage, zlist_maxpage + 1):
        session['nmzpages'].append(i)

    conn.close()
    return render_template('zayavkalist.html', ver=app.version)


# *****************************


@app.route('/add_application/', methods=['GET', 'POST'])
def addapplication():
    return edit_application(-1)


@app.route('/remadd_application/', methods=['POST'])
def addapplicationpost():
    session['errorstr'] = ""
    session['app_id_application'] = request.form['id_application']
    session['app_theme'] = request.form['theme']
    session['app_id_company'] = request.form['comp_app']
    session['app_id_member'] = request.form['user_app']

    session['app_type_sc'] = request.form['type_sc']
    session['app_date_from'] = request.form['date_from']
    session['app_date_to'] = request.form['date_to']

    session['app_dline_issue'] = request.form['dline_issue']
    session['app_dline_decision'] = request.form['dline_decision']

    session['app_descr_konf'] = request.form['descr_konf']
    session['orgcom'] = request.form['orgcom']

    # дополнительная проверка дат на случай отключенных JS
    td_from = date(session['app_date_from'])

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()
    cursor.execute(" select count(*) from members where login=%s and id_member<>%s",
                   (request.form['lgn'], request.form['id_member'],))
    conn.close()

    return render_template('add_application.html', ver=app.version)


@app.route('/edit_z/<int:id_application>', methods=['GET', 'POST'])
def edit_application(id_application):
    au = session.get('is_auth', False)
    if (not au):
        return redirect("/login/")

    if request.method == 'POST':

        try:
            conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                                    password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
            cursor = conn.cursor()
            if (session['app_id_application'] == '-1'):
                cursor.execute(
                    "INSERT INTO application(theme, id_company, id_sciency,     datefrom,                   dateto,              dateatticle,                 datedecision,                  id_member, deleted,describe_conf, orgcom_conf, statusapplication, id_moderator) " + \
                    "VALUES (                 %s,       %s,        %s,              %s,                        %s,                   %s,                          %s,                           %s,       'Н',     %s,              %s,             %s,           %s ) returning id_application;",
                    (
                        request.form['theme'], request.form['comp_app'], request.form['type_sc'],
                        request.form['date_from'],
                        request.form['date_to'], request.form['dline_issue'], request.form['dline_decision'],
                        request.form['user_app'],
                        request.form['descr_konf'],
                        request.form['orgcom'],
                        request.form['statapp'],
                        request.form['moderator'],

                    ))

                conn.commit()
                res = cursor.fetchall()
            else:
                sqlstr="update application set theme=%s, id_company=%s, id_sciency=%s, datefrom=%s, dateto=%s, dateatticle=%s, datedecision=%s, id_member=%s, describe_conf=%s,orgcom_conf=%s , statusapplication=%s , id_moderator=%s" + \
                    "where id_application="+str(session['app_id_application'])
                cursor.execute(sqlstr,
                    (
                        request.form['theme'], request.form['comp_app'], request.form['type_sc'],

                        request.form['date_from'],
                        request.form['date_to'], request.form['dline_issue'], request.form['dline_decision'],
                        request.form['user_app'],
                        request.form['descr_konf'],
                        request.form['orgcom'],
                        request.form['statapp'],
                        request.form['moderator'],

                    ))
                conn.commit()


        except Exception:
            return "Ошибка при записи"

        conn.close()
        return redirect("/zlist/1")
    else:
        conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                                password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
        cursor = conn.cursor()

        cursor.execute(
            "select id_member, famely||' '||name||' '||surname from members where (deleted<>'Д' or deleted is null) order by 2")

        session.app_members = cursor.fetchall()

        cursor.execute("select id_dict,name from dict where dict_name='орг' order by name")

        session.app_companies = cursor.fetchall()

        cursor.execute("select id_dict,name from dict where dict_name='рнаук' order by name")
        session.app_types_sc = cursor.fetchall()


#
        session['app_statapps']=[[0,'на рассмотрении'],[1,'одобрена'],[2,'отказано']]
#



        if (id_application == -1):
            session['app_id_application'] = '-1'
            session['app_theme'] = ''
            session['app_id_company'] = session['comp_nm']
            session['app_company'] = session['comp_nm']
            session['app_id_member'] = session['id_member']
            session['app_username'] = session['fml'] + ' ' + session['nm'] + ' ' + session['sn']
            session['app_statapp'] = 0
            session['app_id_mod'] = session['id_member']
            session['app_disabled'] = ''

        else:
            #                  0               1       2            3          4        5             6            7            8             9               10            11          12                    13
            sqlstr = "select id_application, theme, id_company, id_sciency, datefrom, dateto, statusapplication, id_member, dateatticle, datedecision, describe_conf, orgcom_conf, statusapplication , id_moderator " + \
                     "from application where id_application=" + str(id_application)

            cursor.execute(sqlstr)
            if cursor.rowcount < 1:
                session['errorstr'] = "SQl-не найден id_application=" + id_application
                return redirect("/error/")

            res_app = cursor.fetchall()

            session['errorstr'] = ""
            session['app_id_application'] = id_application
            session['app_theme'] = res_app[0][1]
            session['app_id_company'] = res_app[0][2]
            session['app_id_member'] = res_app[0][7]
            session['app_type_sc'] = res_app[0][3]
            session['app_date_from'] = res_app[0][4]
            session['app_date_to'] = res_app[0][5]

            session['app_dline_issue'] = res_app[0][8]
            session['app_dline_decision'] = res_app[0][9]

            session['app_descr_konf'] = res_app[0][10]
            session['app_orgcom'] = res_app[0][11]
            session['app_statapp'] = res_app[0][12]
            session['app_id_mod'] = res_app[0][13]

            if session['app_statapp']>=1:
                session['app_disabled']='disabled'
            else:
                session['app_disabled']=''


        conn.close()
        return render_template('add_application.html', ver=app.version)


@app.route('/edit_profil/')
def edit_profil():
    return render_template('Registry.html', ver=app.version, regim='edit')


@app.route('/edit_profil/', methods=['POST'])
def write_profil():
    return write_registry()


@app.route('/deletez/<int:id_application>', methods=['GET', 'POST'])
def delete_app(id_application: int):

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])

    cursor = conn.cursor()
    if app_may_delete(id_application,cursor):
        cursor.execute("delete from application where id_application="+str(id_application))
        conn.commit()
        conn.close()
        return render_template('message.html', ver=app.version, message='Заявка "' + session['app_theme'] + '" Удалена', urlret='location.href="/zlist/1" ')
    else:
        cursor.execute("select theme from application where id_application="+str(id_application))
        res =cursor.fetchall()
        msg='Заявка "' + res[0][0] + '" <br/> Удаление невозможно, свяжитесь с администратором'
        conn.close()
        return render_template('message.html', ver=app.version, message=Markup(msg),urlret='javascript:history.go(-1)')


def app_may_delete(id_app:int, curs) -> bool:
    # определяет допустимо ли удаление заявки

    curs.execute("select count(*) from conf where id_application=" + str(id_app))
    resq=curs.fetchall()
    if resq[0][0]<1:
        res = True
    else:
        res = False

    return res;


#**********************************

@app.route('/conflist/<int:nompage>')
def conflist(nompage:int):

    au = session.get('is_auth', False)
    if (not au):
        return redirect("/login/")
    session['cflist_nompage'] = nompage

    # ***********************
    #                       0             1        2                3                 4       5          6                              7                             8
    sqlstr = "select id_conf, theme, comp.name company, sc.name scname, to_char(datefrom, 'dd.mm.yyyy'), to_char(dateto,'dd.mm.yyyy'), statusconf, to_char(dateatticle,'dd.mm.yyyy')  " + \
             "from conf a left outer join dict comp on (comp.dict_name='орг' and comp.id_dict=a.id_company) " + \
             "left outer join dict sc on (sc.dict_name='онаук' and sc.id_dict=a.id_sciency) " + \
             "where (a.deleted<>'Д' or a.deleted is null) " + \
             "order by datefrom, theme limit " + \
             str(app.lenthuserlistpage) + " offset " + str((session['cflist_nompage'] - 1) * app.lenthuserlistpage)

    conn = psycopg2.connect(host=app.config['HOSTDATABASE'], user=app.config['USERNAME'],
                            password=app.config['PASSWORD'], dbname=app.config['DBNAME'])
    cursor = conn.cursor()

    cursor.execute(sqlstr)

    session.cflist = cursor.fetchall()

    cursor.execute("select count(*) from conf where (deleted<>'Д' or deleted is null)")
    amountrec = cursor.fetchall()[0][0]

    maxpage = (amountrec // app.lenthuserlistpage) + 1

    cflist_minpage = nompage - 5
    if (cflist_minpage < 1):
        cflist_minpage = 1

    cflist_maxpage = nompage + 5
    if (cflist_maxpage > maxpage):
        cflist_maxpage = maxpage

    session['nmcfpages'] = []
    session['maxcfpages'] = cflist_maxpage
    for i in range(cflist_minpage, cflist_maxpage + 1):
        session['nmcfpages'].append(i)

    conn.close()
    return render_template('cflist.html', ver=app.version)



#**********************************

if __name__ == '__main__':
    app.run()

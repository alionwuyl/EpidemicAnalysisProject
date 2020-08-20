import flask
from flask import jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from timeUtil import get_cur_date, get_pre_n_date
import time




app = flask.Flask(__name__)


# app.config为项目的配置字典
# 将SQLAlchemy相关配置加入app
# SQLALCHEMY_DATABASE_URI 配置 SQLAlchemy 的链接字符串
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:wyl5683wyl@localhost:3306/epidemicdb?charset=utf8"
# SQLALCHEMY_POOL_SIZE 配置 SQLAlchemy 的连接池大小
app.config['SQLALCHEMY_POOL_SIZE'] = 5
# SQLALCHEMY_POOL_TIMEOUT 配置 SQLAlchemy 的连接超时时间
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 15
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# 实例化SQLAlchemy
# PS : 实例化SQLAlchemy的代码必须要在引入蓝图之前
db = SQLAlchemy(app)


class ForeignDailyDatas(db.Model):
    __tablename__ = "foreign_daily_datas"
    Id = db.Column(db.Integer, primary_key=True)
    died = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    crued = db.Column(db.Integer)
    area = db.Column(db.String)
    curConfirm = db.Column(db.Integer)
    confirmedRelative = db.Column(db.Integer)
    updatedTime = db.Column(db.String)

    def __repr__(self):
        return '<ForeignDailyDatas>area: %s, curConfirm: %d, confirmed: %d, confirmedRelative: %d, died: %d, crued: %d, pub_date: %s</ForeignDailyDatas>' % (self.area, self.curConfirm, self.confirmed, self.confirmedRelative, self.died, self.cured, self.pub_date)


class ProvinceDailyDatas(db.Model):
    __tablename__ = "province_daily_datas"
    Id = db.Column(db.Integer, primary_key=True)
    curConfirm = db.Column(db.Integer)
    curConfirmRelative = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    confirmedRelative = db.Column(db.Integer)
    died = db.Column(db.Integer)
    diedRelative = db.Column(db.Integer)
    cured = db.Column(db.Integer)
    curedRelative = db.Column(db.Integer)
    area = db.Column(db.String)
    asymptomatic = db.Column(db.Integer)
    asymptomaticRelative = db.Column(db.Integer)
    pub_date = db.Column(db.String)

    def __repr__(self):
        return '<ProvinceDailyDatas>area: %s, curConfirm: %d, curConfirmRelative: %d, confirmed: %d, confirmedRelative: %d, died: %d, diedRelative: %d, cured: %d, curedRelative: %d, asymptomatic: %d, asymptomaticRelative: %d, pub_date: %s</ProvinceDailyDatas>' % (self.area, self.curConfirm, self.curConfirmRelative, self.confirmed, self.confirmedRelative, self.died, self.diedRelative, self.cured, self.curedRelative, self.asymptomatic, self.asymptomaticRelative, self.pub_date)


class CityDailyDatas(db.Model):
    __tablename__ = 'city_daily_datas'
    Id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    confirmedRelative = db.Column(db.Integer)
    curConfirm = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    died = db.Column(db.Integer)
    crued = db.Column(db.Integer)
    pub_date = db.Column(db.String)
    province = db.Column(db.String)

    def __repr__(self):
        return '<CityDailyDatas>city: %s, confirmedRelative: %d, curConfirm: %d, confirmed: %d, died: %d, crued: %d, pub_date: %s, province: %s</CityDailyDatas>' % (self.city, self.confirmedRelative, self.curConfirm, self.confirmed, self.died, self.crued, self.pub_date, self.province)

class HomeRealtimeDatas(db.Model):
    __tablename__ = 'home_realtime_datas'
    Id = db.Column(db.Integer, primary_key=True)
    curConfirm = db.Column(db.Integer)
    curConfirmRelative = db.Column(db.Integer)
    asymptomatic = db.Column(db.Integer)
    asymptomaticRelative = db.Column(db.Integer)
    unconfirmed = db.Column(db.Integer)
    unconfirmedRelative = db.Column(db.Integer)
    icu = db.Column(db.Integer)
    icuRelative = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    confirmedRelative = db.Column(db.Integer)
    overseasInput = db.Column(db.Integer)
    overseasInputRelative = db.Column(db.Integer)
    cured = db.Column(db.Integer)
    curedRelative = db.Column(db.Integer)
    died = db.Column(db.Integer)
    diedRelative = db.Column(db.Integer)
    updatedTime = db.Column(db.String)

    def __repr__(self):
        return '<HomeRealtimeDatas>curConfirm: %d, curConfirmRelative: %d, asymptomatic: %d, asymptomaticRelative: %d, unconfirmed: %d, unconfirmedRelative: %s, icu: %s, icuRelaitve:%s,  confirmed: %d, confirmedRelative: %d, overseasInput: %d, overseasInputRelative: %d, cured: %d, curedRelative: %d, died: %d, diedRelative: %d,\
            updatedTime: %s</HomeRealtimeDatas>' % (self.curConfirm, self.curConfirmRelative, self.asymptomatic, self.asymptomaticRelative, self.unconfirmed, self.unconfirmedRelative, self.icu, self.icuRelative, self.confirmed, self.confirmedRelative, self.overseasInput, self.overseasInputRelative, self.cured, self.curedRelative, self.died, self.diedRelative, self.updatedTime)

class ForeignRealtimeDatas(db.Model):
    __tablename__ = 'foreign_realtime_datas'
    Id = db.Column(db.Integer, primary_key=True)
    curConfirm = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    confirmedRelative = db.Column(db.Integer)
    died = db.Column(db.Integer)
    diedRelative = db.Column(db.Integer)
    cured = db.Column(db.Integer)
    curedRelative = db.Column(db.Integer)
    updatedTime = db.Column(db.String)

    def __repr__(self):
        return '<ForeignRealtimeDatas>curConfirm: %d, confirmed: %d, confirmedRelative: %d, died: %d, diedRelative: %d, crued: %d, curedRelative: %d, pub_date: %s</ForeignRealtimeDatas>' % (self.curConfirm, self.confirmed, self.confirmedRelative, self.died, self.diedRelative, self.cured, self.curedRelative, self.updatedTime)



@app.route('/')
def start():
    return render_template('hello1.html')


# 得到国内疫情数据
@app.route('/get_home_realtime_datas', methods=["GET", "POST"])
def query_home_realtime_datas():
    curdatestr = get_cur_date()  # 当日日期
    results = HomeRealtimeDatas.query.filter(HomeRealtimeDatas.updatedTime.like(curdatestr+'%')).all()

    print('++++ [get_home_realtime_datas]获取国内疫情整体数据date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = HomeRealtimeDatas.query.filter(HomeRealtimeDatas.updatedTime.like(predatestr+'%')).all()

        print('++++ [get_home_realtime_datas]获取国内疫情整体数据date: date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('++++ [get_home_realtime_datas]获取国内疫情整体数据date: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('++++ [get_home_realtime_datas]获取国内疫情整体数据date: 获取不到数据')
    print(results)
    a = jsonify(asymptomatic=results[0].asymptomatic, asymptomaticRelative=results[0].asymptomaticRelative, unconfirmed=results[0].unconfirmed, unconfirmedRelative=results[0].unconfirmedRelative, icu=results[0].icu, icuRelative=results[0].icuRelative, curConfirm=results[0].curConfirm, curConfirmRelative=results[0].curConfirmRelative,  confirmed=results[0].confirmed, confirmedRelative=results[0].confirmedRelative, overseasInput=results[0].overseasInput, overseasInputRelative=results[0].overseasInputRelative,   cured=results[0].cured, curedRelative=results[0].curedRelative, died=results[0].died, diedRelative=results[0].diedRelative, updatedTime=results[0].updatedTime)
    #print(a)
    return a



# 得到国外疫情数据
@app.route('/get_foreign_realtime_datas', methods=["GET", "POST"])
def query_foreign_realtime_datas():
    curdatestr = get_cur_date()  # 当日日期
    results = ForeignRealtimeDatas.query.filter(ForeignRealtimeDatas.updatedTime.like(curdatestr+'%')).all()

    print('++++ [get_foreign_realtime_datas]获取国外疫情整体数据date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ForeignRealtimeDatas.query.filter(ForeignRealtimeDatas.updatedTime.like(predatestr+'%')).all()

        print('++++ [get_foreign_realtime_datas]获取国外疫情整体数据 date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('++++ [get_foreign_realtime_datas]获取国外疫情整体数据 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('++++ [get_foreign_realtime_datas]获取国外疫情整体数据 获取不到数据')
    return jsonify(curConfirm=results[0].curConfirm, confirmed=results[0].confirmed, confirmedRelative=results[0].confirmedRelative, cured=results[0].cured, curedRelative=results[0].curedRelative, died=results[0].died, diedRelative=results[0].diedRelative, updatedTime=results[0].updatedTime)



# 得到所有城市的现有确诊人数
@app.route('/province_curConfirm', methods=["GET", "POST"])
def query_province_curConfirm():
    curdatestr = get_cur_date()  # 当日日期
    results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(curdatestr+'%')).order_by(ProvinceDailyDatas.curConfirm.desc()).all()

    print('++++ [province_curconfirm]获取现有确诊病例数所有省份, date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(predatestr+'%')).order_by(ProvinceDailyDatas.curConfirm.desc()).all()

        print('++++ [province_curconfirm]获取现有确诊病例数所有省份, date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [province_curconfirm]获取现有确诊病例数所有省份: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [province_curconfirm]获取现有确诊病例数所有省份: 获取不到数据')
    return jsonify(pub_date=results[0].pub_date, areas=[x.area for x in results], curConfirms=[x.curConfirm for x in results])

# 得到境外新增输入数据
@app.route('/get_newInOverseasTrends', methods=["GET", "POST"])
def query_new_inoverseas_trends():
    results = HomeRealtimeDatas.query.order_by(HomeRealtimeDatas.updatedTime).limit(5).all()
    print(results)
    
    if len(results) < 5:
        print('数据小于5天')
        return jsonify(pub_date='00', Tdates=[0 for i in range(0,5)], nums=[0 for i in range(0,5)])
    print('获取成功')
    return jsonify(pub_date = results[0].updatedTime, dates=[x.updatedTime[0:10] for x in results], nums=[x.overseasInputRelative for x in results] )

# 得到境外输入数据
@app.route('/get_sumInOverseasTrends', methods=["GET", "POST"])
def query_sum_inoverseas_trends():
    results = HomeRealtimeDatas.query.order_by(HomeRealtimeDatas.updatedTime).limit(5).all()
    print(results)
    
    if len(results) < 5:
        print('数据小于5天')
        return jsonify(pub_date='00', Tdates=[0 for i in range(0,5)], nums=[0 for i in range(0,5)])
    print('获取成功')
    return jsonify(pub_date = results[0].updatedTime, dates=[x.updatedTime[0:10] for x in results], nums=[x.overseasInput for x in results] )


# 数据库中没有境外输入
# 得到境外输入top5数据
@app.route('/get_provinceTop10', methods=["GET", "POST"])
def query_province_overseasInput_top_5():
    curdatestr = get_cur_date()  # 当日日期
    results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(curdatestr+'%')).order_by(ProvinceDailyDatas.overseasInput.desc()).limit(5).all()

    print('++++ [province_overseasInput_top_5]获取无症状新增病例数所有省份, date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(predatestr+'%')).order_by(ProvinceDailyDatas.overseasInput.desc()).limit(5).all()

        print('++++ [province_overseasInput_top_5]获取无症状新增病例数所有省份, date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [province_overseasInput_top_5]获取无症状新增病例数所有省份: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [province_overseasInput_top_5]获取无症状新增病例数所有省份: 获取不到数据')
    return jsonify(pub_date=results[0].pub_date, areas=[x.area for x in results], overseasInput=[x.overseasInput for x in results])

# 获取全国
@app.route('/get_allProvinceNewTrends10', methods=["GET", "POST"])
def query_allprovince_overseasInput():
    results = HomeRealtimeDatas.query.limit(5).all()

    if len(results) < 5:
        print('数据量小于5')
    else:
        print('获取成功')
    print(results)
    a = jsonify(pub_date=results[0].updatedTime, dates=[x.updatedTime for x in results], conConfirmed=[x.confirmedRelative for x in results], overSeasInput=[x.overseasInputRelative for x in results])
    #print(a)
    return a

# 获取全国
@app.route('/get_allProvinceSumTrends10', methods=["GET", "POST"])
def query_allprovince_1():
    results = HomeRealtimeDatas.query.limit(5).all()

    if len(results) < 5:
        print('数据量小于5')
    else:
        print('获取成功')
    print(results)
    a = jsonify(pub_date=results[0].updatedTime, dates=[x.updatedTime for x in results], curComfirm=[x.curConfirm for x in results], uncomfirmed=[x.unconfirmed for x in results], comfirmed=[x.confirmed for x in results])
    #print(a)
    return a

# 获取全国
@app.route('/get_allProvinceDiedCured10', methods=["GET", "POST"])
def query_allprovince_2():
    results = HomeRealtimeDatas.query.limit(5).all()

    if len(results) < 5:
        print('数据量小于5')
    else:
        print('获取成功')
    print(results)
    a = jsonify(pub_date=results[0].updatedTime, dates=[x.updatedTime for x in results], cured=[x.cured for x in results], died=[x.died for x in results], comfirmed=[x.confirmed for x in results])
    #print(a)
    return a

# 得到所有城市的较昨日新增无症状感染者Top5
@app.route('/province_asymptomatic_relative_top_5', methods=["GET", "POST"])
def query_province_asymptomatic_relative_top_5():
    curdatestr = get_cur_date()  # 当日日期
    results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(curdatestr+'%')).order_by(ProvinceDailyDatas.asymptomaticRelative.desc()).limit(5).all()

    print('++++ [province_asymptomatic_relative_top_5]获取无症状新增病例数所有省份, date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(predatestr+'%')).order_by(ProvinceDailyDatas.asymptomaticRelative.desc()).limit(5).all()

        print('++++ [province_asymptomatic_relative_top_5]获取无症状新增病例数所有省份, date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [province_asymptomatic_relative_top_5]获取无症状新增病例数所有省份: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [province_asymptomatic_relative_top_5]获取无症状新增病例数所有省份: 获取不到数据')
    return jsonify(pub_date=results[0].pub_date, areas=[x.area for x in results], asymptomaticRelative=[x.asymptomaticRelative for x in results])




# 获取现有确诊病例数省份Top5
@app.route('/province_curconfirm_top_5', methods=["GET", "POST"])
def query_province_datas():
    curdatestr = get_cur_date()  # 当日日期
    results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(curdatestr+'%')).order_by(ProvinceDailyDatas.curConfirm.desc()).limit(5).all()

    print('++++ [province_curconfirm_top_5]获取现有确诊病例数省份Top5, date: %s,  results length: %d' % (curdatestr, len(results)))
    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(predatestr+'%')).order_by(ProvinceDailyDatas.curConfirm.desc()).limit(5).all()

        print('++++ [province_curconfirm_top_5]获取现有确诊病例数省份Top5, date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [province_curconfirm_top_5]获取现有确诊病例数省份Top5: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [province_curconfirm_top_5]获取现有确诊病例数省份Top5: 获取不到数据')
    print(type(results))
    print(type(results[0]))
    print(results)
    return jsonify(pub_date=results[0].pub_date, areas=[x.area for x in results], curConfirms=[x.curConfirm for x in results])


# 获取现存境外输入最多的省份Top20
@app.route('/query_province_import_datas', methods=["GET", "POST"])
def query_province_import_datas():
    # mydb = MyDB('localhost', 'root', '123456', 'conv19_datas')
    # datas = mydb.province_import_top_n()
    # ret = jsonify(pub_date=datas[0][3], provinces=[x[0] for x in datas], confirmed=[x[1] for x in datas], curConfirms=[x[2] for x in datas])
    curdatestr = get_cur_date()  # 当日日期
    results = CityDailyDatas.query.filter(CityDailyDatas.pub_date.like(curdatestr+'%'), CityDailyDatas.city.like('境外输入%')).order_by(CityDailyDatas.confirmed.desc()).limit(20).all()

    print('++++ [query_province_import_datas]获取现存境外输入最多的省份Top20 date: %s,  results length: %d' % (curdatestr, len(results)))

    n = 1
    targetdate = curdatestr

    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = CityDailyDatas.query.filter(CityDailyDatas.pub_date.like(predatestr+'%'), CityDailyDatas.city.like('境外输入%')).order_by(CityDailyDatas.confirmed.desc()).limit(20).all()

        print('++++ [query_province_import_datas]获取现存境外输入最多的省份Top20 date: %s,  results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [query_province_import_datas]获取现存境外输入最多的省份Top20: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [query_province_import_datas]获取现存境外输入最多的省份Top20: 获取不到数据')

    return jsonify(pub_date=results[0].pub_date, provinces=[x.province for x in results], confirmed=[x.confirmed for x in results], curConfirms=[x.curConfirm for x in results])


# 获取最近一日全国各个省份的现有确诊人数
@app.route('/query_province_curConfirms_data', methods=['GET', 'POST'])
def get_province_curConfirm_datas():
    curdatestr = get_cur_date()  # 当日日期
    results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.like(curdatestr+'%')).all()

    print('++++ [get_province_curConfirm_datas]获取最近一日全国各个省份的现有确诊人数 date: %s,  results length: %d' % (curdatestr, len(results)))

    n = 1
    targetdate = curdatestr
    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = ProvinceDailyDatas.query.filter(ProvinceDailyDatas.pub_date.startswith(predatestr+'%')).all()

        print('+++ [get_province_curConfirm_datas]获取最近一日全国各个省份的现有确诊人数 predatestr: %s, results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break

    if len(results) > 0:
        print('+++ [get_province_curConfirm_datas]获取最近一日全国各个省份的现有确诊人数: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [get_province_curConfirm_datas]获取最近一日全国各个省份的现有确诊人数: 获取不到数据')

    return jsonify(pub_date=results[0].pub_date, areas=[x.area for x in results], curConfirms=[x.curConfirm for x in results])


def process_city_name(city_name):
    ret = ''
    pos1 = city_name.find("地区")
    pos2 = city_name.find("区")
    if pos1 >= 0:
        ret = city_name[: pos1]
    elif pos2 >= 0:
        ret = city_name[: pos2]
    else:
        ret = city_name
    return ret


# 获取各个城市现有确诊人数
@app.route('/query_cities_curconfirm', methods=['GET', 'POST'])
def get_cities_curconfirm():
    curdatestr = get_cur_date()
    results = CityDailyDatas.query.filter(CityDailyDatas.pub_date.like(curdatestr + '%'), CityDailyDatas.city.notlike('境外输入%')).filter(CityDailyDatas.curConfirm > 0).all()

    print('++++ [get_cities_curconfirm]获取最近一日全国各城市的现有确诊人数 date: %s,  results length: %d' % (curdatestr, len(results)))

    n = 1
    targetdate = curdatestr
    while len(results) <= 0:
        predatestr = get_pre_n_date(n)
        results = CityDailyDatas.query.filter(CityDailyDatas.pub_date.like(predatestr + '%'), CityDailyDatas.city.notlike('境外输入%')).filter(CityDailyDatas.curConfirm > 0).all()

        print('+++ [get_cities_curconfirm]获取最近一日全国各城市的现有确诊人数 predatestr: %s, results length: %d' % (predatestr, len(results)))

        n += 1
        if len(results) > 0:
            targetdate = predatestr
        else:
            time.sleep(2)  # 休眠2s
        if n > 100:
            print('+++ [mydb] 最近三个月都没有数据')
            targetdate = ''
            break
    if len(results) > 0:
        print('+++ [get_cities_curconfirm]获取最近一日全国各城市的现有确诊人数: 获取到%s的数据，数量：%d' % (targetdate, len(results)))
    else:
        print('+++ [get_cities_curconfirm]获取最近一日全国各城市的现有确诊人数: 获取不到数据')

    datas = []
    for i in range(len(results)):
        datas.append({'name': process_city_name(results[i].city), 'value': results[i].curConfirm})

    return jsonify(pub_date=results[0].pub_date, datas=datas)


# 获取近N日全国新增确诊病例情况
@app.route('/query_inside_confirm_increasement')
def get_inside_confirm_increasement():
    pass


@app.route('/query_city_datas')
def query_city_datas():
    return '查询地级市数据...'








































if __name__ == '__main__':
    # host='0.0.0.0', port=8888
    app.run(debug=True)
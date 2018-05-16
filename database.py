from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tables import *
from datetime import date

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def book_entry(isbn, book_name, author, publisher, publish_year_month, librarian_id, book_id, location):
    librarian = db_session.query(Librarian).filter(Librarian.id == librarian_id).first()
    cip = db_session.query(CIP).filter(CIP.isbn == isbn).first()
    if cip is None:
        cip = CIP(isbn=isbn, book_name=book_name, author=author, publisher=publisher, publish_year_month=publish_year_month, librarian=librarian)

    status = BookStatus.available if location == '图书流通室' else BookStatus.unborrowable
    book = Book(id=book_id, cip=cip, location=location, status=status, librarian=librarian)

    db_session.add(book)
    db_session.commit()


def populate_data():
    librarian1 = Librarian(id='lib0001', name='张三', password='lib0001')
    librarian2 = Librarian(id='lib0002', name='李四', password='lib0002')
    librarian3 = Librarian(id='lib0003', name='王五', password='lib0003')

    reader1 = Reader(id='rea0001', name='李明', password='rea0001', tel='18800201111', email='18800201111@163.com')
    reader2 = Reader(id='rea0002', name='刘晓明', password='rea0002', tel='18800202222', email='18800202222@163.com')
    reader3 = Reader(id='rea0003', name='张颖', password='rea0003', tel='18800203333', email='18800203333@163.com')
    reader4 = Reader(id='rea0004', name='谭卓然', password='rea0004', tel='18800200539', email='Jerome1997@iCloud.com')

    cip1 = CIP(isbn='ISBN7-302-02368-9', book_name='数据结构', author='严蔚敏 吴伟民', publisher='清华大学出版社',
               publish_year_month=date(year=1997, month=4, day=1), librarian=librarian1)
    cip2 = CIP(isbn='ISBN7-302-02357-1', book_name='数据库使用教程', author='董建全', publisher='清华大学出版社',
               publish_year_month=date(year=2016, month=4, day=1), librarian=librarian1)

    book1 = Book(id='C832.1', cip=cip1, location='图书流通室', status=BookStatus.available, librarian=librarian1)
    book2 = Book(id='C832.2', cip=cip1, location='图书流通室', status=BookStatus.available, librarian=librarian1)
    book3 = Book(id='C832.3', cip=cip1, location='图书流通室', status=BookStatus.available, librarian=librarian1)
    book4 = Book(id='C832.4', cip=cip1, location='图书阅览室', status=BookStatus.unborrowable, librarian=librarian1)

    book5 = Book(id='C357.1', cip=cip2, location='图书流通室', status=BookStatus.available, librarian=librarian1)
    book6 = Book(id='C357.2', cip=cip2, location='图书流通室', status=BookStatus.available, librarian=librarian1)

    db_session.add_all([librarian1, librarian2, librarian3,
                        reader1, reader2, reader3, reader4,
                        cip1, cip2,
                        book1, book2, book3, book4, book5, book6])
    db_session.commit()

    book_entry('ISBN9-787-53998-1', '巨人的陨落', '[英]肯·福莱特', '江苏凤凰文艺出版社', date(year=2015, month=5, day=1), 'lib0001',
               'C787.1', '图书流通室')
    book_entry('ISBN9-787-53998-1', '巨人的陨落', '[英]肯·福莱特', '江苏凤凰文艺出版社', date(year=2015, month=5, day=1), 'lib0001',
               'C787.2', '图书流通室')
    book_entry('ISBN9-787-53998-1', '巨人的陨落', '[英]肯·福莱特', '江苏凤凰文艺出版社', date(year=2015, month=5, day=1), 'lib0001',
               'C787.3', '图书流通室')

    book_entry('ISBN9-101-17892-2', '百年孤独', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2011, month=6, day=1), 'lib0001',
               'C101.1', '图书流通室')
    book_entry('ISBN9-101-17892-2', '百年孤独', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2011, month=6, day=1), 'lib0001',
               'C101.2', '图书流通室')
    book_entry('ISBN9-101-17892-2', '百年孤独', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2011, month=6, day=1), 'lib0001',
               'C101.3', '图书流通室')
    book_entry('ISBN9-101-17892-2', '百年孤独', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2011, month=6, day=1), 'lib0001',
               'C101.4', '图书流通室')

    book_entry('ISBN9-102-15732-6', '追风筝的人', '[美]卡勒德·胡赛尼', '上海人民出版社', date(year=2006, month=5, day=1), 'lib0001',
               'C102.1', '图书流通室')
    book_entry('ISBN9-102-15732-6', '追风筝的人', '[美]卡勒德·胡赛尼', '上海人民出版社', date(year=2006, month=5, day=1), 'lib0001',
               'C102.2', '图书流通室')
    book_entry('ISBN9-102-15732-6', '追风筝的人', '[美]卡勒德·胡赛尼', '上海人民出版社', date(year=2006, month=5, day=1), 'lib0001',
               'C102.3', '图书流通室')

    book_entry('ISBN9-103-89422-3', '霍乱时期的爱情', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2012, month=9, day=1), 'lib0001',
               'C103.1', '图书流通室')
    book_entry('ISBN9-103-89422-3', '霍乱时期的爱情', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2012, month=9, day=1), 'lib0001',
               'C103.2', '图书流通室')
    book_entry('ISBN9-103-89422-3', '霍乱时期的爱情', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2012, month=9, day=1), 'lib0001',
               'C103.3', '图书流通室')
    book_entry('ISBN9-103-89422-3', '霍乱时期的爱情', '[哥伦比亚]加西亚·马尔克斯', '南海出版公司', date(year=2012, month=9, day=1), 'lib0001',
               'C103.4', '图书流通室')

    book_entry('ISBN9-104-23529-5', '新名字的故事', '[意]埃莱娜·费兰特', '人民文学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C104.1', '图书流通室')
    book_entry('ISBN9-104-23529-5', '新名字的故事', '[意]埃莱娜·费兰特', '人民文学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C104.2', '图书流通室')
    book_entry('ISBN9-104-23529-5', '新名字的故事', '[意]埃莱娜·费兰特', '人民文学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C104.3', '图书流通室')

    book_entry('ISBN9-105-36265-1', '雪落香杉树', '[美]戴维·伽特森', '人民文学出版社', date(year=2017, month=6, day=1), 'lib0001',
               'C105.1', '图书流通室')
    book_entry('ISBN9-105-36265-1', '雪落香杉树', '[美]戴维·伽特森', '人民文学出版社', date(year=2017, month=6, day=1), 'lib0001',
               'C105.2', '图书流通室')

    book_entry('ISBN9-106-35268-9', '1984', '[英]乔治·奥威尔', '北京十月文艺出版社', date(year=2010, month=4, day=1), 'lib0001',
               'C106.1', '图书流通室')
    book_entry('ISBN9-106-35268-9', '1984', '[英]乔治·奥威尔', '北京十月文艺出版社', date(year=2010, month=4, day=1), 'lib0001',
               'C106.2', '图书流通室')
    book_entry('ISBN9-106-35268-9', '1984', '[英]乔治·奥威尔', '北京十月文艺出版社', date(year=2010, month=4, day=1), 'lib0001',
               'C106.3', '图书流通室')

    book_entry('ISBN9-107-75325-4', '鱼王', '[俄]维克托·阿斯塔菲耶夫', '广西师范大学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C107.1', '图书流通室')
    book_entry('ISBN9-107-75325-4', '鱼王', '[俄]维克托·阿斯塔菲耶夫', '广西师范大学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C107.2', '图书流通室')
    book_entry('ISBN9-107-75325-4', '鱼王', '[俄]维克托·阿斯塔菲耶夫', '广西师范大学出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C107.3', '图书流通室')

    book_entry('ISBN9-108-83685-7', '月亮和六便士', '[英]毛姆', '上海译文出版社', date(year=2006, month=8, day=1), 'lib0001', 'C108.1',
               '图书流通室')
    book_entry('ISBN9-108-83685-7', '月亮和六便士', '[英]毛姆', '上海译文出版社', date(year=2006, month=8, day=1), 'lib0001', 'C108.2',
               '图书流通室')
    book_entry('ISBN9-108-83685-7', '月亮和六便士', '[英]毛姆', '上海译文出版社', date(year=2006, month=8, day=1), 'lib0001', 'C108.3',
               '图书流通室')

    book_entry('ISBN9-109-39257-7', '活着', '余华', '南海出版公司', date(year=1998, month=5, day=1), 'lib0001', 'C109.1', '图书流通室')
    book_entry('ISBN9-109-39257-7', '活着', '余华', '南海出版公司', date(year=1998, month=5, day=1), 'lib0001', 'C109.2', '图书流通室')
    book_entry('ISBN9-109-39257-7', '活着', '余华', '南海出版公司', date(year=1998, month=5, day=1), 'lib0001', 'C109.3', '图书流通室')

    book_entry('ISBN9-110-76593-3', '杀死一只知更鸟', '[美]哈珀·李', '译林出版社', date(year=2012, month=9, day=1), 'lib0001', 'C110.1',
               '图书流通室')
    book_entry('ISBN9-110-76593-3', '杀死一只知更鸟', '[美]哈珀·李', '译林出版社', date(year=2012, month=9, day=1), 'lib0001', 'C110.2',
               '图书流通室')
    book_entry('ISBN9-110-76593-3', '杀死一只知更鸟', '[美]哈珀·李', '译林出版社', date(year=2012, month=9, day=1), 'lib0001', 'C110.3',
               '图书流通室')

    book_entry('ISBN9-111-93786-2', '囚鸟', '[美]库尔特·冯内古特', '百花洲文艺出版社', date(year=2017, month=6, day=1), 'lib0001',
               'C111.1', '图书流通室')
    book_entry('ISBN9-111-93786-2', '囚鸟', '[美]库尔特·冯内古特', '百花洲文艺出版社', date(year=2017, month=6, day=1), 'lib0001',
               'C111.2', '图书流通室')
    book_entry('ISBN9-111-93786-2', '囚鸟', '[美]库尔特·冯内古特', '百花洲文艺出版社', date(year=2017, month=6, day=1), 'lib0001',
               'C111.3', '图书流通室')

    book_entry('ISBN9-112-98467-9', '局外人', '[法]阿尔贝·加缪', '上海译文出版社', date(year=2010, month=9, day=1), 'lib0001', 'C112.1',
               '图书流通室')
    book_entry('ISBN9-112-98467-9', '局外人', '[法]阿尔贝·加缪', '上海译文出版社', date(year=2010, month=9, day=1), 'lib0001', 'C112.2',
               '图书流通室')
    book_entry('ISBN9-112-98467-9', '局外人', '[法]阿尔贝·加缪', '上海译文出版社', date(year=2010, month=9, day=1), 'lib0001', 'C112.3',
               '图书流通室')

    book_entry('ISBN5-310-89456-3', '万历十五年', '[美]黄仁宇', '生活·读书·新知三联书店', date(year=1997, month=5, day=1), 'lib0001',
               'C310.1', '图书流通室')
    book_entry('ISBN5-310-89456-3', '万历十五年', '[美]黄仁宇', '生活·读书·新知三联书店', date(year=1997, month=5, day=1), 'lib0001',
               'C310.2', '图书流通室')
    book_entry('ISBN5-310-89456-3', '万历十五年', '[美]黄仁宇', '生活·读书·新知三联书店', date(year=1997, month=5, day=1), 'lib0001',
               'C310.3', '图书流通室')

    book_entry('ISBN5-311-45812-4', '中国历代政治得失', '钱穆', '生活·读书·新知三联书店', date(year=2001, month=5, day=1), 'lib0001',
               'C311.1', '图书流通室')
    book_entry('ISBN5-311-45812-4', '中国历代政治得失', '钱穆', '生活·读书·新知三联书店', date(year=2001, month=5, day=1), 'lib0001',
               'C311.2', '图书流通室')
    book_entry('ISBN5-311-45812-4', '中国历代政治得失', '钱穆', '生活·读书·新知三联书店', date(year=2001, month=5, day=1), 'lib0001',
               'C311.3', '图书流通室')

    book_entry('ISBN5-312-90845-1', '大国的崩溃', '[美]沙希利·浦洛基', '四川人民出版社', date(year=2017, month=5, day=1), 'lib0001',
               'C312.1', '图书流通室')
    book_entry('ISBN5-312-90845-1', '大国的崩溃', '[美]沙希利·浦洛基', '四川人民出版社', date(year=2017, month=5, day=1), 'lib0001',
               'C312.2', '图书流通室')
    book_entry('ISBN5-312-90845-1', '大国的崩溃', '[美]沙希利·浦洛基', '四川人民出版社', date(year=2017, month=5, day=1), 'lib0001',
               'C312.3', '图书流通室')

    book_entry('ISBN5-313-78560-4', '海洋与文明', '[美]林肯·佩恩', '天津人民出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C313.1', '图书流通室')
    book_entry('ISBN5-313-78560-4', '海洋与文明', '[美]林肯·佩恩', '天津人民出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C313.2', '图书流通室')
    book_entry('ISBN5-313-78560-4', '海洋与文明', '[美]林肯·佩恩', '天津人民出版社', date(year=2017, month=4, day=1), 'lib0001',
               'C313.3', '图书流通室')

    book_entry('ISBN5-314-75689-7', '明朝那些事儿', '当年明月', '中国海关出版社', date(year=2009, month=4, day=1), 'lib0001', 'C314.1',
               '图书流通室')
    book_entry('ISBN5-314-75689-7', '明朝那些事儿', '当年明月', '中国海关出版社', date(year=2009, month=4, day=1), 'lib0001', 'C314.2',
               '图书流通室')
    book_entry('ISBN5-314-75689-7', '明朝那些事儿', '当年明月', '中国海关出版社', date(year=2009, month=4, day=1), 'lib0001', 'C314.3',
               '图书流通室')

    book_entry('ISBN5-315-68504-5', '十二幅地图中的世界史', '[英]杰里·布罗顿', '浙江人民出版社', date(year=2016, month=6, day=1), 'lib0001',
               'C315.1', '图书流通室')
    book_entry('ISBN5-315-68504-5', '十二幅地图中的世界史', '[英]杰里·布罗顿', '浙江人民出版社', date(year=2016, month=6, day=1), 'lib0001',
               'C315.2', '图书流通室')
    book_entry('ISBN5-315-68504-5', '十二幅地图中的世界史', '[英]杰里·布罗顿', '浙江人民出版社', date(year=2016, month=6, day=1), 'lib0001',
               'C315.3', '图书流通室')

    book_entry('ISBN5-316-89056-8', '天朝的崩溃', '茅海建', '生活·读书·新知三联书店', date(year=2005, month=7, day=1), 'lib0001',
               'C316.1', '图书流通室')
    book_entry('ISBN5-316-89056-8', '天朝的崩溃', '茅海建', '生活·读书·新知三联书店', date(year=2005, month=7, day=1), 'lib0001',
               'C316.2', '图书流通室')
    book_entry('ISBN5-316-89056-8', '天朝的崩溃', '茅海建', '生活·读书·新知三联书店', date(year=2005, month=7, day=1), 'lib0001',
               'C316.3', '图书流通室')

    book_entry('ISBN5-317-89056-8', '史记', '司马迁', '中华书局', date(year=1982, month=11, day=1), 'lib0001', 'C317.1', '图书流通室')
    book_entry('ISBN5-317-89056-8', '史记', '司马迁', '中华书局', date(year=1982, month=11, day=1), 'lib0001', 'C317.2', '图书流通室')
    book_entry('ISBN5-317-89056-8', '史记', '司马迁', '中华书局', date(year=1982, month=11, day=1), 'lib0001', 'C317.3', '图书流通室')

    book_entry('ISBN5-318-70456-4', '大英博物馆世界简史', '[英]尼尔·麦格雷戈', '新星出版社', date(year=2014, month=1, day=1), 'lib0001',
               'C318.1', '图书流通室')
    book_entry('ISBN5-318-70456-4', '大英博物馆世界简史', '[英]尼尔·麦格雷戈', '新星出版社', date(year=2014, month=1, day=1), 'lib0001',
               'C318.2', '图书流通室')
    book_entry('ISBN5-318-70456-4', '大英博物馆世界简史', '[英]尼尔·麦格雷戈', '新星出版社', date(year=2014, month=1, day=1), 'lib0001',
               'C318.3', '图书流通室')

    book_entry('ISBN1-630-89745-2', '经济学原理', '[美]曼昆', '机械工业出版社', date(year=2013, month=8, day=1), 'lib0001', 'C630.1',
               '图书流通室')
    book_entry('ISBN1-630-89745-2', '经济学原理', '[美]曼昆', '机械工业出版社', date(year=2013, month=8, day=1), 'lib0001', 'C630.2',
               '图书流通室')
    book_entry('ISBN1-630-89745-2', '经济学原理', '[美]曼昆', '机械工业出版社', date(year=2013, month=8, day=1), 'lib0001', 'C630.3',
               '图书流通室')

    book_entry('ISBN1-631-56098-6', '通往奴役之路', '[英]弗里德利希·奥古斯特·哈耶克', '中国社会科学出版社', date(year=1997, month=8, day=1),
               'lib0001', 'C631.1', '图书流通室')
    book_entry('ISBN1-631-56098-6', '通往奴役之路', '[英]弗里德利希·奥古斯特·哈耶克', '中国社会科学出版社', date(year=1997, month=8, day=1),
               'lib0001', 'C631.2', '图书流通室')
    book_entry('ISBN1-631-56098-6', '通往奴役之路', '[英]弗里德利希·奥古斯特·哈耶克', '中国社会科学出版社', date(year=1997, month=8, day=1),
               'lib0001', 'C631.3', '图书流通室')

    book_entry('ISBN1-632-78564-1', '国富论', '[英]亚当·斯密', '华夏出版社', date(year=2005, month=1, day=1), 'lib0001', 'C632.1',
               '图书流通室')
    book_entry('ISBN1-632-78564-1', '国富论', '[英]亚当·斯密', '华夏出版社', date(year=2005, month=1, day=1), 'lib0001', 'C632.2',
               '图书流通室')
    book_entry('ISBN1-632-78564-1', '国富论', '[英]亚当·斯密', '华夏出版社', date(year=2005, month=1, day=1), 'lib0001', 'C632.3',
               '图书流通室')

    book_entry('ISBN1-633-86097-3', '激荡十三年', '吴晓波', '中信出版社', date(year=2007, month=1, day=1), 'lib0001', 'C633.1',
               '图书流通室')
    book_entry('ISBN1-633-86097-3', '激荡十三年', '吴晓波', '中信出版社', date(year=2007, month=1, day=1), 'lib0001', 'C633.2',
               '图书流通室')
    book_entry('ISBN1-633-86097-3', '激荡十三年', '吴晓波', '中信出版社', date(year=2007, month=1, day=1), 'lib0001', 'C633.3',
               '图书流通室')

    book_entry('ISBN1-634-98124-2', '大国大城', '陆铭', '上海人民出版社', date(year=2016, month=7, day=1), 'lib0001', 'C634.1',
               '图书流通室')
    book_entry('ISBN1-634-98124-2', '大国大城', '陆铭', '上海人民出版社', date(year=2016, month=7, day=1), 'lib0001', 'C634.2',
               '图书流通室')
    book_entry('ISBN1-634-98124-2', '大国大城', '陆铭', '上海人民出版社', date(year=2016, month=7, day=1), 'lib0001', 'C634.3',
               '图书流通室')

    book_entry('ISBN3-790-66580-5', '三体', '刘慈欣', '重庆出版社', date(year=2008, month=1, day=1), 'lib0001', 'C790.1', '图书流通室')
    book_entry('ISBN3-790-66580-5', '三体', '刘慈欣', '重庆出版社', date(year=2008, month=1, day=1), 'lib0001', 'C790.2', '图书流通室')
    book_entry('ISBN3-790-66580-5', '三体', '刘慈欣', '重庆出版社', date(year=2008, month=1, day=1), 'lib0001', 'C790.3', '图书流通室')

    book_entry('ISBN3-791-79145-1', '你一生的故事', '[美]特德·姜', '译林出版社', date(year=2015, month=5, day=1), 'lib0001', 'C791.1',
               '图书流通室')
    book_entry('ISBN3-791-79145-1', '你一生的故事', '[美]特德·姜', '译林出版社', date(year=2015, month=5, day=1), 'lib0001', 'C791.2',
               '图书流通室')
    book_entry('ISBN3-791-79145-1', '你一生的故事', '[美]特德·姜', '译林出版社', date(year=2015, month=5, day=1), 'lib0001', 'C791.3',
               '图书流通室')

    book_entry('ISBN3-792-89675-5', '献给阿尔吉侬的花束', '[美]丹尼尔·凯斯', '辽宁教育出版社', date(year=2005, month=8, day=1), 'lib0001',
               'C792.1', '图书流通室')
    book_entry('ISBN3-792-89675-5', '献给阿尔吉侬的花束', '[美]丹尼尔·凯斯', '辽宁教育出版社', date(year=2005, month=8, day=1), 'lib0001',
               'C792.2', '图书流通室')
    book_entry('ISBN3-792-89675-5', '献给阿尔吉侬的花束', '[美]丹尼尔·凯斯', '辽宁教育出版社', date(year=2005, month=8, day=1), 'lib0001',
               'C792.3', '图书流通室')

    book_entry('ISBN3-793-67890-2', '沙丘', '[美]弗兰克·赫伯特', '江苏凤凰文艺出版社', date(year=2017, month=2, day=1), 'lib0001',
               'C793.1', '图书流通室')
    book_entry('ISBN3-793-67890-2', '沙丘', '[美]弗兰克·赫伯特', '江苏凤凰文艺出版社', date(year=2017, month=2, day=1), 'lib0001',
               'C793.2', '图书流通室')
    book_entry('ISBN3-793-67890-2', '沙丘', '[美]弗兰克·赫伯特', '江苏凤凰文艺出版社', date(year=2017, month=2, day=1), 'lib0001',
               'C793.3', '图书流通室')

    book_entry('ISBN3-794-36758-1', '看海的人', '[日]小林泰三', '新星出版社', date(year=2015, month=2, day=1), 'lib0001', 'C794.1',
               '图书流通室')
    book_entry('ISBN3-794-36758-1', '看海的人', '[日]小林泰三', '新星出版社', date(year=2015, month=2, day=1), 'lib0001', 'C794.2',
               '图书流通室')
    book_entry('ISBN3-794-36758-1', '看海的人', '[日]小林泰三', '新星出版社', date(year=2015, month=2, day=1), 'lib0001', 'C794.3',
               '图书流通室')

    book_entry('ISBN3-795-80945-9', '海底两万里', '[法]儒尔·凡尔纳', '译林出版社', date(year=2002, month=9, day=1), 'lib0001', 'C795.1',
               '图书流通室')
    book_entry('ISBN3-795-80945-9', '海底两万里', '[法]儒尔·凡尔纳', '译林出版社', date(year=2002, month=9, day=1), 'lib0001', 'C795.2',
               '图书流通室')
    book_entry('ISBN3-795-80945-9', '海底两万里', '[法]儒尔·凡尔纳', '译林出版社', date(year=2002, month=9, day=1), 'lib0001', 'C795.3',
               '图书流通室')

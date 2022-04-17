from selenium import webdriver
from selenium.webdriver.edge.options import Options
from lxml import etree
import time
from selenium.webdriver.common.by import By


def conserve_1(dict1,dict2):
    with open('每日数据.txt','a',encoding='utf-8') as fp:
        fp.writelines(str(time.strftime("%Y-%B-%d",time.localtime()))+'\n')
        fp.writelines(str(dict1)+'\n')
        fp.writelines(str(dict2)+'\n')

def conserve_2(data):
    with open('诉求数据.txt','w',encoding='utf-8') as fp:
        fp.writelines(data)


def daily_get():
    edge_option = Options()
    edge_option.add_argument('--headless')
    edge_option.add_argument('--disable-gpu')

    proceeding_daily = {}
    percentage = {}
    bro = webdriver.Edge(options=edge_option)
    bro.get('http://www.sh12345.gov.cn/')
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    sort_data_list = tree.xpath('//*[@id="chartdiv"]/div/div/svg/g[9]//text()')
    sort_list = tree.xpath('/html/body/div[6]/div/div[1]//text()')
    sort_data = [each[1:] for each in sort_data_list]
    for n in range(len(sort_data)):
        percentage[sort_list[2*n+1]] = sort_data[n]
    data_list = tree.xpath('//*[@id="chartdiv2"]/div/div/svg/g[6]/g//@aria-label')
    data = [each[2:] for each in data_list]
    name_list = tree.xpath('/html/body/div[6]/div/div[3]/div[2]//text()')
    for i in range(len(data_list)):
        proceeding_daily[name_list[2*i+1]] = data[i]
    conserve_1(percentage,proceeding_daily)
    bro.quit()
    #daily_time()

def get_inmassage(bro):
    page = bro.page_source
    tree = etree.HTML(page)
    pro_list = tree.xpath('//ul[@id="appealList"]/li/div/a')
    original_widow = bro.current_window_handle
    for pro in range(len(pro_list)):
        data = {"诉求标题":None,"提交时间":None,"诉求内容":None,"办结时间":None,"办结回复":None}
        href = pro_list[pro].xpath('./@href')[0]
        bro.execute_script(f'window.open("{href}","_blank");')
        time.sleep(3)
        windows = bro.window_handles
        bro.switch_to.window(windows[-1])
        in_page = bro.page_source
        tree = etree.HTML(in_page)
        data["诉求标题"] = tree.xpath('//*[@id="appTitle"]/text()')[0]
        data["提交时间"] = tree.xpath('//*[@id="appStartTime"]/text()')[0]
        data["诉求内容"] = tree.xpath('//*[@id="appContent"]/text()')[0]
        data["办结时间"] = tree.xpath('//*[@id="appCreateTime"]/text()')[0]
        data["办结回复"] = tree.xpath('//*[@id="appReply"]/text()')[0]
        datas.append(str(data)+'\n\n')
        bro.close()
        bro.switch_to.window(original_widow)

def proceeding_get():
    #edge_option = Options()
    #edge_option.add_argument('--headless')
    #edge_option.add_argument('--disable-gpu')

    #bro = webdriver.Edge(options=edge_option)
    bro = webdriver.Edge()
    bro.get('http://www.sh12345.gov.cn/r/cms/www/shline12345/appeal_public.html')
    time.sleep(2)
    get_inmassage(bro)
    print("第1页爬取成功！")
    xpath = '//*[@id="pagnation"]/a[3]'
    for i in range(19):
        bro.find_element(By.XPATH,xpath).click()
        time.sleep(2)
        windows = bro.window_handles
        bro.switch_to.window(windows[-1])
        get_inmassage(bro)
        print("第{}页爬取成功！".format(i+2))
    time.sleep(3)
    bro.quit()

def main():
    daily_get()
    #proceeding_get()

if __name__ == '__main__':
    datas = []
    main()
    #conserve_2(datas)
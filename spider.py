import requests
import numpy
from nonce_hkey_encrypto import *

cookies = {
    # 'x_xhh_tokenid': 'BPQKGvIl10l+nOmsA8oaUUZQiButW4B3E/nC4YVXKQ6lp4s1XWk2/yr7PoU1Hj0/lGtfc/YgjvCGhSjhigGzbCA%3D%3D',
}


def nah(link_id):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://www.xiaoheihe.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.xiaoheihe.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    }
    base_param = D('/bbs/app/link/tree', str(time_int + 1), md5_string)

    intro_ = {
        'os_type': 'web',
        'version': '999.0.3',
        'x_app': 'heybox_website',
        'x_client_type': 'web',
        'x_os_type': 'Windows',
        'link_id': link_id,
        'limit': '20',
        'offset': '0',
        'owner_only': '0',
        'sort_filter': 'hot',
    }
    base_param.update(intro_)
    print('开始获取全部楼层的用户信息')
    response = requests.get('https://api.xiaoheihe.cn/bbs/app/link/tree', params=base_param, cookies=cookies,
                            headers=headers)
    comments = {}

    def get_comments(response_json):
        for i in response_json['result']['comments']:
            floor_num = i['comment'][0]['floor_num']
            user_id = i['comment'][0]['user']['userid']
            user_name = i['comment'][0]['user']['username']
            comments[user_id] = {'层数': floor_num, '用户名': user_name}

    response_json = response.json()
    total_floor_num = response_json.get("total_floor_num")

    def get_all_page_info(total_floor_nums):
        for i in range(20, total_floor_nums, 20):
            base_param['offset'] = i
            response = requests.get('https://api.xiaoheihe.cn/bbs/app/link/tree', params=base_param, cookies=cookies,
                                    headers=headers)
            response_json = response.json()
            get_comments(response_json)

    total_page = response_json.get("total_page")
    get_comments(response_json)
    get_all_page_info(total_floor_num)
    print("开始抽奖")
    user_id_list = [i for i in comments.keys()]
    choice_user_id = numpy.random.choice(user_id_list, 1, replace=False)[0]
    user_info = comments.get(choice_user_id)
    print('-------抽奖结果-------')
    print("文章ID：", base_param['link_id'])
    print("总页数：", total_page)
    print("总评论数：", total_floor_num)
    print(f'开奖时间（北京时间）：{arrow.now().format("YYYY-MM-DD HH:mm:ss")}')
    print(f'用户名：{user_info["用户名"]}，用户ID：{choice_user_id}，评论层数：{user_info["层数"]}')


if __name__ == "__main__":
    content_url = input('小黑盒文章网址(输入后回车)：\n').strip()
    print("正在获取文章ID")
    link_id = re.findall('/list/(\d+)', content_url)
    if link_id:
        print("文章ID为：",link_id[0])
        link_id = link_id[0]
        nah(link_id)
    else:
        print("文章ID获取失败")


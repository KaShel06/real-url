# 获取抖音直播的真实流媒体地址

import re
import sys
import requests


class DouYin:
    def __init__(self, url_input):
        self.debug = False
        self.url_input = url_input
        self.room_id = None
        self.headers = {
            'authority': 'v.douyin.com',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }
        
    def get_room_id(self):
        if re.match(r'\d{19}', self.url_input):
            self.room_id = self.url_input
            return True
        
        try:
            url = re.search(r'(https.*)', self.url_input).group(1)
            response = requests.head(url, headers=self.headers)
            url = response.headers['location']
            self.room_id = re.search(r'\d{19}', url).group(0)
            return True
        except Exception as e:
            if self.debug:
                print(e)
            raise Exception('获取room_id失败')
            
    def get_real_url(self):
        if not self.room_id and not self.get_room_id():
            return False
        
        try:
            self.headers.update({
                'authority': 'webcast.amemv.com',
                'cookie': '_tea_utm_cache_1128={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}',
            })

            params = (
                ('type_id', '0'),
                ('live_id', '1'),
                ('room_id', self.room_id),
                ('app_id', '1128'),
            )

            response = requests.get('https://webcast.amemv.com/webcast/room/reflow/info/', 
                                   headers=self.headers, params=params).json()

            rtmp_pull_url = response['data']['room']['stream_url']['rtmp_pull_url']
            hls_pull_url = response['data']['room']['stream_url']['hls_pull_url']
            
            return {
                'rtmp_url': rtmp_pull_url,
                'hls_url': hls_pull_url
            }
        except Exception as e:
            if self.debug:
                print(e)
            raise Exception('获取real url失败')


def get_real_url(rid):
    try:
        douyin = DouYin(rid)
        return douyin.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    url_input = input('请输入抖音直播链接或19位room_id：')
    result = get_real_url(url_input)
    
    if result:
        print('room_id', result.get('room_id', ''))
        print(result.get('rtmp_url', ''))
        print(result.get('hls_url', ''))

from genshinhelper import config

from .basenotifier import BaseNotifier
from ..utils import log, req


class WechatWorkApp(BaseNotifier):
    def __init__(self):
        self.name = 'Wechat Work App'
        self.token = config.WW_APP_AGENTID if self.access_token and config.WW_APP_AGENTID else ''
        self.retcode_key = 'errcode'
        self.retcode_value = 0

    @property
    def access_token(self):
        if config.WW_ID and config.WW_APP_SECRET:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
            data = {'corpid': config.WW_ID, 'corpsecret': config.WW_APP_SECRET}

            try:
                response = req.request('get', url, params=data).json()
            except Exception as e:
                log.error(e)
            else:
                retcode = response.get('errcode')
                if retcode == 0:
                    return response['access_token']
                else:
                    log.error(f'access_token 获取失败:\n{response}')
                    return
        else:
            return

    def send(self, text='Genshin Impact Helper', status='status', desp='desp'):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'
        data = {
            'touser': config.WW_APP_USERID,
            'msgtype': 'text',
            'agentid': config.WW_APP_AGENTID,
            'text': {
                'content': f'{text} {status}\n\n{desp}'
            }
        }
        return self.push('post', url, json=data)
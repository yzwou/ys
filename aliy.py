# services/oss.py
import oss2
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import requests
from alibabacloud_openapi_util.client import Client as util
from tea.request import TeaRequest

accessKeyId = 'LTAI5tPVbMmWsFhQ3AxV3jg9'
accessKeySecret = 'lB2fCK6eVsFiU8G08mth99yeqOUfyc'
securityToken = None

bucket_name = 'winjava21'
region = 'oss-cn-hangzhou'  # Bucket 所在区域

class OSSClient:
    def __init__(self):
        endpoint = f"https://{region}.aliyuncs.com"
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)


    def get_signed_url(self, local_path, remote_name, expire=3600):
        remote_name = str(remote_name)
        self.bucket.put_object_from_file(remote_name, local_path)
        return self.bucket.sign_url("GET", remote_name, expire)


    def download(self, local_path, remote_name):
        self.bucket.get_object_to_file(remote_name, local_path)


class FcClient:
    def __init__(self):
        method = 'POST'
        url = 'https://enkacard-qsspclkjbz.ap-southeast-1.fcapp.run'  # 你的HTTP触发器地址
        date = datetime.utcnow().isoformat('T')[:19] + 'Z'
        headers = {
            'x-acs-date': date,
            'x-acs-security-token': securityToken
        }
        self.headers = headers
        self.url = url
        parsedUrl = urlparse(url)
        authRequest = TeaRequest()
        authRequest.method = method
        authRequest.pathname = parsedUrl.path.replace('$', '%24')
        authRequest.headers = headers
        authRequest.query = {k: v[0] for k, v in parse_qs(parsedUrl.query).items()}
        auth = util.get_authorization(authRequest, 'ACS3-HMAC-SHA256', '', accessKeyId, accessKeySecret)
        headers['authorization'] = auth


    def card(self, uid: str, character_id: str):
        body = {
            "uid": uid,
            "character_id": character_id
        }
        resp = requests.post(self.url, json=body, headers=self.headers)
        return resp.json()


if __name__ == '__main__':
    oss = OSSClient()
    oss.download("269377658_100000472.png", "269377658_10000047.png", expire=3600)

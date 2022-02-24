import os
import re
import logging
import requests
import hashlib

SPREADSHEET_URL = 'https://opensheet.elk.sh/1Y4qoXTpd0ZO2CRZzgYV3Lvd1Aihui_Ya6p0V89nKdNU/Unique%20Codes'
EARLY_ACCESS_DENIED_MD5 = 'ignore'

logger = logging.getLogger(__name__)


def find_next_filename(filename):
    counter = 1
    path, name = os.path.split(filename)
    new_name = os.path.join(path, '%s-%s' % (counter, name))
    while os.path.exists(new_name):
        counter += 1
        new_name = os.path.join(path, '%s-%s' % (counter, name))
    return new_name


def download_file(url):
    logger.info('Fetching %s', url)
    local_filename = os.path.join('imgs', url.split('/')[-1])
    if os.path.exists(local_filename):
        with open(local_filename, 'rb') as f:
            existing_hash = hashlib.md5(f.read())
    else:
        existing_hash = ''
    try:
        with requests.get(url) as r:
            r.raise_for_status()
            new_hash = hashlib.md5(r.content).hexdigest()
            if new_hash == existing_hash or new_hash == EARLY_ACCESS_DENIED_MD5:
                return
            if existing_hash and existing_hash != new_hash and existing_hash != EARLY_ACCESS_DENIED_MD5:
                backup_filename = find_next_filename(local_filename)
                os.rename(local_filename, backup_filename)
                logger.warning('Image hash changed for existing file.  Backing up %s to %s', local_filename, backup_filename)
            with open(local_filename, 'wb') as f:
                f.write(r.content)
    except requests.exceptions.HTTPError as e:
        logger.error('%s', e)


def main():
    os.makedirs('imgs', exist_ok=True)
    sheet_json = requests.get(SPREADSHEET_URL).json()
    url_re = re.compile('^https://www.bungie.net/pubassets/wqarg/strips/[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}.png')
    image_urls = [x['Image Link'] for x in sheet_json if url_re.match(x['Image Link'])]
    # image_urls = jmespath.search(SRC_JMES_FILTER, sheet_json)
    for url in image_urls:
        print(url)
        download_file(url)


if __name__ == "__main__":
    main()
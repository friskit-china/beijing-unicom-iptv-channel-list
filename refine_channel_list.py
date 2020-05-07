channel_dict = dict()

f = open('bj-unicom-iptv.m3u').read().splitlines()
name_replace_dict = {
    '＋': '+',
    'HD': '高清'
}

post_rename_dict = {
    '旅游卫视': '海南卫视'
}

channel_name_list = open('channel_names.lst').read().splitlines()

channel_name2id = dict([[item, idx] for idx, item in enumerate(channel_name_list)])

item_list = [[f[i].split(',')[1], f[i + 1]] for i in range( 2, len(f), 3)]

for item in item_list:
    channel_name = item[0]
    channel_url = item[1]
    for k, v in name_replace_dict.items():
        channel_name = channel_name.replace(k, v)
    try:
        if '高清' in channel_name:
            stem_channel_name = channel_name.strip('高清')
            channel_dict[stem_channel_name] = {
                'name': stem_channel_name,
                'id': channel_name2id[stem_channel_name],
                'url': channel_url
            }
        else:
            if channel_name not in channel_dict:
                channel_dict[channel_name] = {
                    'name': channel_name,
                    'id': channel_name2id[channel_name],
                    'url': channel_url
                }
    except KeyError as e:
        print('发现新频道{e}，请修改"channel_names.lst"频道列表文件'.format(e=e))

item_list = [[post_rename_dict.get(v['name'], v['name']), v['id'], v['url']] for v in channel_dict.values()]

sorted_item_list = sorted(item_list, key=lambda item: item[1])
open('sorted.m3u', 'w').write('\n'.join(['#EXTM3U name="bj-unicom-iptv"\n'] + ['#EXTINF:-1,{t}\n{r}\n'.format(t=item[0], r=item[2]) for item in sorted_item_list]))



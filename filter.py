def filter(words):
    remove_list = ['js', 'www', 'end', 'com', 'experience', 'software',
                   'product', 'understanding', 'requirements', 'resume',
                   'review', 'service', 'development', 'sovs', 'bit', 'ly',
                   'idus', 'pr', 'mvp', 'store', 'framework', 'co', 'kr',
                   'spa', 'page', 'help', 'tool', 'web', 'types', 'years',
                   'net', 'learning', 'text', 'music', 'data', 'science',
                   'etc', 'scientist', 'content', 'contents', 'camp', 'TV',
                   'Biz', 'time', 'team', 'gb', 'kb', 'pro', 'shooting',
                   'desktop', 'engine', 'it', 'boot', 'lee', 'linkedin',
                   'seung', 'kook', 'lee', 'pdf', 'cto', 'cpo', 'ceo',
                   ]
    new_list = []
    for i, word in enumerate(words):
        word = word.lower()
        if word in remove_list:
            words[i] = ''
        elif word == 'back':
            words[i] = 'Backend'
        elif word == 'front':
            words[i] = 'Frontend'
        elif word == 'rest':
            words[i] = 'RESTful'
        elif word == 'native':
            words[i] = 'React Native'
        elif word == 'node':
            words[i] = 'Node.js'
        elif word == 'machine':
            words[i] = 'Machine learning'
        elif word == 'deep':
            words[i] = 'Deep learning'
        elif word == 'trouble':
            words[i] = 'Trouble Shooting'
        elif word == 'unreal':
            words[i] = 'Unreal engine'
        elif word == 'cry':
            words[i] = 'Cry engine'
    new_list = [x for x in words if x]
    return new_list

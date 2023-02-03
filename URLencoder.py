def decoder(string):
    if isinstance(string, str):
        results = string.replace('%', '')
        results = bytes.fromhex(results).decode('utf-8')
        return results
    else:
        return 'value not string'


def encoder(string):
    if isinstance(string, str):
        results = string.encode('utf-8')
        results = str(results).upper().replace('\X', '%').strip('\'B')
        return results
    else:
        return 'value not string'


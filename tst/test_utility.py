import redis_constants


def generate_input(str_list):
    response = b'*' + str(len(str_list)).encode() + redis_constants.LINE_BREAK.encode()
    for element in str_list:
        response += b'$' + str(len(element)).encode()
        response += redis_constants.LINE_BREAK.encode()
        response += element.encode()
        response += redis_constants.LINE_BREAK.encode()

    return response

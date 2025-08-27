from subprocess import check_output

class IP_lezen:
    def __init__(self):
        pass

    def ip_uitlezen(self):
        #***LCD Status ip tonen***
        ips = check_output(['hostname', '--all-ip-addresses'])
        # print(ips)
        ips_string_zonden_b_en_newline = ips.decode('utf-8').strip()
        # print(ips_string_zonden_b_en_newline)
        lijst_ip = ips_string_zonden_b_en_newline.split()
        return lijst_ip
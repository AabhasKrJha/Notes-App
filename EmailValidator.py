def check_mail(email):

    if email.count('@') > 1:  # email as a whole must have only 1 @
        return False
    else:
        # now we saparete('name','@','domain')
        name, symbol, domain_name = email.partition('@')

        # now check each part except symbol , i.e. , @ symbol
        if name == '' or name.strip() == '':
            checked_name = 'invalid'
        else:
            for i in name:
                if i.isalpha() == False:
                    if i.isdigit() == False:
                        if i in ['.', '_']:
                            checked_name = 'valid'
                        else:
                            checked_name = 'invalid'
                            break
                    else:
                        checked_name = 'valid'
                else:
                    checked_name = 'valid'

        # now we will check the domain name

        if domain_name.count('.') > 1:
            checked_domain = 'invalid'
        else:
            domain = domain_name.partition('.')
            Domain = list(domain)
            Domain.pop(1)
            small_letters = list()
            for z in range(97, 97+26):
                small_letters.append(chr(z))

            for k in Domain:
                if k == "" or k.strip() == '':
                    checked_domain = 'invalid'
                else:
                    for l in k:
                        if l not in small_letters:
                            checked_domain = 'invalid'
                        else:
                            checked_domain = 'valid'

    if checked_name == 'valid' and checked_domain == 'valid':
        return True
    else:
        return False

class email_string():
    """
    This is a helper class that takes in a GiftRecipient (or two of them) and returns an email message email_string
    The passed in GiftRecipient is taken in this format:
    ['first_name', 'last_name', 'email', 'street_address', 'city', 'state', 'zip_code']
    """

    def __init__(self, giver, gift_recipient=None):
        self.giver = giver
        self.gift_recipient = gift_recipient

    def entry_message(self):
        ret_str = f"Hello {self.giver['first_name']} {self.giver['last_name']},\n\n"
        ret_str += 'Your information has been saved in the Hoenigmann-Molina Secret Santa database!\n\n'
        ret_str += 'When the time comes, you will receive an email from this account with your Secret Santa recipient, along with their address!\n\n'
        ret_str += 'At the same time, someone else will be sent your address, so that they know where to send your awesome gift!\n\n'
        ret_str += 'Until Christmas Time,\n'
        ret_str += 'Your Friendly Neighborhood Developer ( A.K.A. Alec Hoenigmann :) )'

        return ret_str

    def operation_message(self, gift_recipient=None):
        if self.gift_recipient is None:
            self.gift_recipient = gift_recipient

        ret_str = f"Hello {self.giver['first_name']} {self.giver['last_name']},\n\n"
        ret_str += 'That time has finally arrived!\n\n'
        ret_str += "It's Christmas Time, and it's time to play Secret Santa!\n\n"
        ret_str += 'Your recipient is:\n\n'
        ret_str += f"{self.gift_recipient['first_name']} {self.gift_recipient['last_name']}\n"
        ret_str += f"{self.gift_recipient['street_address']}\n"
        ret_str += f"{self.gift_recipient['city']}, {self.gift_recipient['state']}, {self.gift_recipient['zip_code']}\n\n"
        ret_str += "Be sure to pick out a great gift, and send it ANONYMOUSLY. It's kind of the whole point of Secret Santa.\n\n"
        ret_str += 'With that said, have a Merry Christmas and enjoy your time with your family!\n\n'
        ret_str += 'Until Next Year,\n'
        ret_str += 'Your Friendly Neighborhood Developer ( A.K.A. Alec Hoenigmann :) )'

        return ret_str

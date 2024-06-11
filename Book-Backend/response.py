class Message:
    @staticmethod
    def format_message(message, success, body=None):
        if body:
            return {
                'message': message,
                'success': success,
                'data': body
            }
        else:
            return {
                'message': message,
                'success': success,
            }

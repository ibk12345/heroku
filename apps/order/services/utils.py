from django.core.mail import send_mail

def send_order_confirmation(email):
    
    message=f'''
            Your order was accepted
            '''
    send_mail(
    'Order confirmation', 
    message, 
    'test@gmail.com', 
    [email, ]
    )

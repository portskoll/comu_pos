
import smtplib
def enviar_email(email, texto):

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("portskoll@gmail.com", "jhqgnjefisfjlhff")
        server.sendmail("apinext@mundotela.net", email, texto)
        server.quit()
        return True

    except Exception as e:
        print("Erro ao enviar email:", str(e))
        return False



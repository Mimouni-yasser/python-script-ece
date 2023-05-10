import sys
import yagmail
import pdfkit as pdf

if(__name__ == "__main__"):
    if(len(sys.argv) == 3):
        content = content.replace("//NAME_TO_REPLACE//", sys.argv[1])
        content = content.replace("//SOURCE_TO_REPLACE//", sys.argv[2])
        try:
            f = open("mail.html", "w")
            f.write(content)
        except:
            print("Error while writing to file")
            exit(1)
        yg = yagmail.SMTP("yasmimouni2@gmail.com", "msgppgzwxuxoesix")
        yg.send(to='yasmimouni2@gmail.com', subject='test', contents="./mail.html")
        
    else:
        print("usage: python setupmail.py <name> <image source>")
        exit(1)

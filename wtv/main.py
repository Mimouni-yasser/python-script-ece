import yagmail


#setup yagmail client
c = yagmail.SMTP("ensam.career.expo@gmail.com", "wqpsawkfpmnlyaom")

recipients = ["m.zrikem@uca.ma",
"abdelghafour.atlas@gmail.com",
"a.tajer@uca.ma",
"amassaq@yahoo.com",
"n_idboufker@yahoo.fr",
"elbaamrani@uca.ac.ma",
"r.elassali@uca.ma",
"h.elkabtane@uca.ac.ma",
"l.goujdami@uca.ac.ma",
"lahmaim@gmail.com",
"chiny@uca.ma",
"m.boulouird@uca.ac.ma",
"elbeidsaid@yahoo.fr",
"hatim.anas@gmail.com",
"s.belkouch@uca.ma",
"l.elbahir@uca.ma",
"a.elbacha@uca.ac.ma",
"a.hamzaoui@uca.ma",
"zboulghasoul@gmail.com"
]

#f = open("invitation profs.html", "r")
#contents = f.read()

c.send(to="anfassi26@gmail.com", subject="invitation", contents=yagmail.inline("invitation profs.html"), attachments="./Descriptif de ECE'2 2023.pdf")
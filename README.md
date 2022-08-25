# A script to parse emails in Python

In Python, parsing emails using the email package can sometimes be tricky. For example, the Body of a raw email may not have the "Body" tag, etc. this complicates things.

I developed this script to parse an email account and process its emails according to a series of characteristics.

The script will process every email of the account and depending on the email criteria, will copy, save the data, or delete every email.

It will then save the results to a json file, so all data is preserved.

Also, once the script ends, it will print on-screen a report where the user can check what has happened with every email, so you can verify that the numbers presented and the results check out.

You can use this script as it is now or adapt it to your own needs.

What is included in the script is enough to give you a good idea of how things work and how they can be tweaked to your own needs.

Hope you find this helpful!

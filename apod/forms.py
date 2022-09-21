from django import forms
import datetime
current_year = datetime.datetime.now().year
# print(now+1)

YEARS= [x for x in range(2012,current_year+1)]

class UserForm(forms.Form):
    date= forms.DateField(label='Date',initial="2012-08-06", widget=forms.SelectDateWidget(years=YEARS))
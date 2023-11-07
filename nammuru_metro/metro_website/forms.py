from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RechargeForm(forms.Form):
    amount = forms.CharField(max_length=10)

class LineForm(forms.Form):
    from_choice = forms.ChoiceField(choices=[('purple', 'Purple'), ('green', 'Green')])

class StationForm(forms.Form):
    from_choice = forms.ChoiceField(choices=[("Attiguppe","Attiguppe"),("Baiyappanahalli","Baiyappanahalli"),("Banashankari","Banashankari"),("Benniganahalli","Benniganahalli"),("Challaghatta","Challaghatta"),("Chickpete","Chickpete"),("Cubbon Park","Cubbon Park"),("Dasarahalli","Dasarahalli"),("Deepanjali Nagar","Deepanjali Nagar"),("Doddakallasandra","Doddakallasandra"),("Dr. B. R. Ambedkar Station, Vidhana Soudha","Dr. B. R. Ambedkar Station, Vidhana Soudha"),("Garudacharapalya","Garudacharapalya"),("Goraguntepalya","Goraguntepalya"),("Halasuru","Halasuru"),("Hoodi","Hoodi"),("Hopefarm Channasandra","Hopefarm Channasandra"),("Indiranagar","Indiranagar"),("Jalahalli","Jalahalli"),("Jayanagar","Jayanagar"),("Jayaprakash Nagar","Jayaprakash Nagar"),("Jnanabharathi","Jnanabharathi"),("Kadugodi Tree Park","Kadugodi Tree Park"),("Kengeri","Kengeri"),("Kengeri Bus Terminal","Kengeri Bus Terminal"),("Konanakunte Cross","Konanakunte Cross"),("Krantivira Sangolli Rayanna Railway Station","Krantivira Sangolli Rayanna Railway Station"),("Krishna Rajendra Market","Krishna Rajendra Market"),("Krishnarajapura (K.R.Pura)","Krishnarajapura (K.R.Pura)"),("Kundalahalli","Kundalahalli"),("Lalbagh","Lalbagh"),("Magadi Road","Magadi Road"),("Mahakavi Kuvempu Road","Mahakavi Kuvempu Road"),("Mahalakshmi","Mahalakshmi"),("Mahatma Gandhi Road","Mahatma Gandhi Road"),("Mantri Square Sampige Road","Mantri Square Sampige Road"),("Mysore Road","Mysore Road"),("Nadaprabhu Kempegowda Station, Majestic","Nadaprabhu Kempegowda Station, Majestic"),("Nagasandra","Nagasandra"),("Nallurhalli","Nallurhalli"),("National College","National College"),("Pantharapalya - Nayandahalli","Pantharapalya - Nayandahalli"),("Pattanagere","Pattanagere"),("Pattandur Agrahara","Pattandur Agrahara"),("Peenya","Peenya"),("Peenya Industry","Peenya Industry"),("Rajajinagar","Rajajinagar"),("Rajarajeshwari Nagar","Rajarajeshwari Nagar"),("Rashtreeya Vidyalaya Road","Rashtreeya Vidyalaya Road"),("Sandal Soap Factory","Sandal Soap Factory"),("Seetharampalya","Seetharampalya"),("Silk Institute","Silk Institute"),("Singayyanapalya","Singayyanapalya"),("Sir.M.Visvesvaraya Stn., Central College","Sir.M.Visvesvaraya Stn., Central College"),("South End Circle","South End Circle"),("Sri Balagangadharanatha Swamiji Station, Hosahalli","Sri Balagangadharanatha Swamiji Station, Hosahalli"),("Sri Sathya Sai Hospital","Sri Sathya Sai Hospital"),("Srirampura","Srirampura"),("Swami Vivekananda Road","Swami Vivekananda Road"),("Thalaghattapura","Thalaghattapura"),("Trinity","Trinity"),("Vajarahalli","Vajarahalli"),("Vijayanagar","Vijayanagar"),("Whitefield (Kadugodi)","Whitefield (Kadugodi)"),("Yelachenahalli","Yelachenahalli"),("Yeshwanthpur","Yeshwanthpur")])

class RouteForm(forms.Form):
    entry_choice = forms.ChoiceField(choices=[("Attiguppe","Attiguppe"),("Baiyappanahalli","Baiyappanahalli"),("Banashankari","Banashankari"),("Benniganahalli","Benniganahalli"),("Challaghatta","Challaghatta"),("Chickpete","Chickpete"),("Cubbon Park","Cubbon Park"),("Dasarahalli","Dasarahalli"),("Deepanjali Nagar","Deepanjali Nagar"),("Doddakallasandra","Doddakallasandra"),("Dr. B. R. Ambedkar Station, Vidhana Soudha","Dr. B. R. Ambedkar Station, Vidhana Soudha"),("Garudacharapalya","Garudacharapalya"),("Goraguntepalya","Goraguntepalya"),("Halasuru","Halasuru"),("Hoodi","Hoodi"),("Hopefarm Channasandra","Hopefarm Channasandra"),("Indiranagar","Indiranagar"),("Jalahalli","Jalahalli"),("Jayanagar","Jayanagar"),("Jayaprakash Nagar","Jayaprakash Nagar"),("Jnanabharathi","Jnanabharathi"),("Kadugodi Tree Park","Kadugodi Tree Park"),("Kengeri","Kengeri"),("Kengeri Bus Terminal","Kengeri Bus Terminal"),("Konanakunte Cross","Konanakunte Cross"),("Krantivira Sangolli Rayanna Railway Station","Krantivira Sangolli Rayanna Railway Station"),("Krishna Rajendra Market","Krishna Rajendra Market"),("Krishnarajapura (K.R.Pura)","Krishnarajapura (K.R.Pura)"),("Kundalahalli","Kundalahalli"),("Lalbagh","Lalbagh"),("Magadi Road","Magadi Road"),("Mahakavi Kuvempu Road","Mahakavi Kuvempu Road"),("Mahalakshmi","Mahalakshmi"),("Mahatma Gandhi Road","Mahatma Gandhi Road"),("Mantri Square Sampige Road","Mantri Square Sampige Road"),("Mysore Road","Mysore Road"),("Nadaprabhu Kempegowda Station, Majestic","Nadaprabhu Kempegowda Station, Majestic"),("Nagasandra","Nagasandra"),("Nallurhalli","Nallurhalli"),("National College","National College"),("Pantharapalya - Nayandahalli","Pantharapalya - Nayandahalli"),("Pattanagere","Pattanagere"),("Pattandur Agrahara","Pattandur Agrahara"),("Peenya","Peenya"),("Peenya Industry","Peenya Industry"),("Rajajinagar","Rajajinagar"),("Rajarajeshwari Nagar","Rajarajeshwari Nagar"),("Rashtreeya Vidyalaya Road","Rashtreeya Vidyalaya Road"),("Sandal Soap Factory","Sandal Soap Factory"),("Seetharampalya","Seetharampalya"),("Silk Institute","Silk Institute"),("Singayyanapalya","Singayyanapalya"),("Sir.M.Visvesvaraya Stn., Central College","Sir.M.Visvesvaraya Stn., Central College"),("South End Circle","South End Circle"),("Sri Balagangadharanatha Swamiji Station, Hosahalli","Sri Balagangadharanatha Swamiji Station, Hosahalli"),("Sri Sathya Sai Hospital","Sri Sathya Sai Hospital"),("Srirampura","Srirampura"),("Swami Vivekananda Road","Swami Vivekananda Road"),("Thalaghattapura","Thalaghattapura"),("Trinity","Trinity"),("Vajarahalli","Vajarahalli"),("Vijayanagar","Vijayanagar"),("Whitefield (Kadugodi)","Whitefield (Kadugodi)"),("Yelachenahalli","Yelachenahalli"),("Yeshwanthpur","Yeshwanthpur")])

    exit_choice = forms.ChoiceField(choices=[("Attiguppe","Attiguppe"),("Baiyappanahalli","Baiyappanahalli"),("Banashankari","Banashankari"),("Benniganahalli","Benniganahalli"),("Challaghatta","Challaghatta"),("Chickpete","Chickpete"),("Cubbon Park","Cubbon Park"),("Dasarahalli","Dasarahalli"),("Deepanjali Nagar","Deepanjali Nagar"),("Doddakallasandra","Doddakallasandra"),("Dr. B. R. Ambedkar Station, Vidhana Soudha","Dr. B. R. Ambedkar Station, Vidhana Soudha"),("Garudacharapalya","Garudacharapalya"),("Goraguntepalya","Goraguntepalya"),("Halasuru","Halasuru"),("Hoodi","Hoodi"),("Hopefarm Channasandra","Hopefarm Channasandra"),("Indiranagar","Indiranagar"),("Jalahalli","Jalahalli"),("Jayanagar","Jayanagar"),("Jayaprakash Nagar","Jayaprakash Nagar"),("Jnanabharathi","Jnanabharathi"),("Kadugodi Tree Park","Kadugodi Tree Park"),("Kengeri","Kengeri"),("Kengeri Bus Terminal","Kengeri Bus Terminal"),("Konanakunte Cross","Konanakunte Cross"),("Krantivira Sangolli Rayanna Railway Station","Krantivira Sangolli Rayanna Railway Station"),("Krishna Rajendra Market","Krishna Rajendra Market"),("Krishnarajapura (K.R.Pura)","Krishnarajapura (K.R.Pura)"),("Kundalahalli","Kundalahalli"),("Lalbagh","Lalbagh"),("Magadi Road","Magadi Road"),("Mahakavi Kuvempu Road","Mahakavi Kuvempu Road"),("Mahalakshmi","Mahalakshmi"),("Mahatma Gandhi Road","Mahatma Gandhi Road"),("Mantri Square Sampige Road","Mantri Square Sampige Road"),("Mysore Road","Mysore Road"),("Nadaprabhu Kempegowda Station, Majestic","Nadaprabhu Kempegowda Station, Majestic"),("Nagasandra","Nagasandra"),("Nallurhalli","Nallurhalli"),("National College","National College"),("Pantharapalya - Nayandahalli","Pantharapalya - Nayandahalli"),("Pattanagere","Pattanagere"),("Pattandur Agrahara","Pattandur Agrahara"),("Peenya","Peenya"),("Peenya Industry","Peenya Industry"),("Rajajinagar","Rajajinagar"),("Rajarajeshwari Nagar","Rajarajeshwari Nagar"),("Rashtreeya Vidyalaya Road","Rashtreeya Vidyalaya Road"),("Sandal Soap Factory","Sandal Soap Factory"),("Seetharampalya","Seetharampalya"),("Silk Institute","Silk Institute"),("Singayyanapalya","Singayyanapalya"),("Sir.M.Visvesvaraya Stn., Central College","Sir.M.Visvesvaraya Stn., Central College"),("South End Circle","South End Circle"),("Sri Balagangadharanatha Swamiji Station, Hosahalli","Sri Balagangadharanatha Swamiji Station, Hosahalli"),("Sri Sathya Sai Hospital","Sri Sathya Sai Hospital"),("Srirampura","Srirampura"),("Swami Vivekananda Road","Swami Vivekananda Road"),("Thalaghattapura","Thalaghattapura"),("Trinity","Trinity"),("Vajarahalli","Vajarahalli"),("Vijayanagar","Vijayanagar"),("Whitefield (Kadugodi)","Whitefield (Kadugodi)"),("Yelachenahalli","Yelachenahalli"),("Yeshwanthpur","Yeshwanthpur")])

class TicketBuyForm(forms.Form):
    start_station = forms.ChoiceField(choices=[("Attiguppe","Attiguppe"),("Baiyappanahalli","Baiyappanahalli"),("Banashankari","Banashankari"),("Benniganahalli","Benniganahalli"),("Challaghatta","Challaghatta"),("Chickpete","Chickpete"),("Cubbon Park","Cubbon Park"),("Dasarahalli","Dasarahalli"),("Deepanjali Nagar","Deepanjali Nagar"),("Doddakallasandra","Doddakallasandra"),("Dr. B. R. Ambedkar Station, Vidhana Soudha","Dr. B. R. Ambedkar Station, Vidhana Soudha"),("Garudacharapalya","Garudacharapalya"),("Goraguntepalya","Goraguntepalya"),("Halasuru","Halasuru"),("Hoodi","Hoodi"),("Hopefarm Channasandra","Hopefarm Channasandra"),("Indiranagar","Indiranagar"),("Jalahalli","Jalahalli"),("Jayanagar","Jayanagar"),("Jayaprakash Nagar","Jayaprakash Nagar"),("Jnanabharathi","Jnanabharathi"),("Kadugodi Tree Park","Kadugodi Tree Park"),("Kengeri","Kengeri"),("Kengeri Bus Terminal","Kengeri Bus Terminal"),("Konanakunte Cross","Konanakunte Cross"),("Krantivira Sangolli Rayanna Railway Station","Krantivira Sangolli Rayanna Railway Station"),("Krishna Rajendra Market","Krishna Rajendra Market"),("Krishnarajapura (K.R.Pura)","Krishnarajapura (K.R.Pura)"),("Kundalahalli","Kundalahalli"),("Lalbagh","Lalbagh"),("Magadi Road","Magadi Road"),("Mahakavi Kuvempu Road","Mahakavi Kuvempu Road"),("Mahalakshmi","Mahalakshmi"),("Mahatma Gandhi Road","Mahatma Gandhi Road"),("Mantri Square Sampige Road","Mantri Square Sampige Road"),("Mysore Road","Mysore Road"),("Nadaprabhu Kempegowda Station, Majestic","Nadaprabhu Kempegowda Station, Majestic"),("Nagasandra","Nagasandra"),("Nallurhalli","Nallurhalli"),("National College","National College"),("Pantharapalya - Nayandahalli","Pantharapalya - Nayandahalli"),("Pattanagere","Pattanagere"),("Pattandur Agrahara","Pattandur Agrahara"),("Peenya","Peenya"),("Peenya Industry","Peenya Industry"),("Rajajinagar","Rajajinagar"),("Rajarajeshwari Nagar","Rajarajeshwari Nagar"),("Rashtreeya Vidyalaya Road","Rashtreeya Vidyalaya Road"),("Sandal Soap Factory","Sandal Soap Factory"),("Seetharampalya","Seetharampalya"),("Silk Institute","Silk Institute"),("Singayyanapalya","Singayyanapalya"),("Sir.M.Visvesvaraya Stn., Central College","Sir.M.Visvesvaraya Stn., Central College"),("South End Circle","South End Circle"),("Sri Balagangadharanatha Swamiji Station, Hosahalli","Sri Balagangadharanatha Swamiji Station, Hosahalli"),("Sri Sathya Sai Hospital","Sri Sathya Sai Hospital"),("Srirampura","Srirampura"),("Swami Vivekananda Road","Swami Vivekananda Road"),("Thalaghattapura","Thalaghattapura"),("Trinity","Trinity"),("Vajarahalli","Vajarahalli"),("Vijayanagar","Vijayanagar"),("Whitefield (Kadugodi)","Whitefield (Kadugodi)"),("Yelachenahalli","Yelachenahalli"),("Yeshwanthpur","Yeshwanthpur")])

    end_station = forms.ChoiceField(choices=[("Attiguppe","Attiguppe"),("Baiyappanahalli","Baiyappanahalli"),("Banashankari","Banashankari"),("Benniganahalli","Benniganahalli"),("Challaghatta","Challaghatta"),("Chickpete","Chickpete"),("Cubbon Park","Cubbon Park"),("Dasarahalli","Dasarahalli"),("Deepanjali Nagar","Deepanjali Nagar"),("Doddakallasandra","Doddakallasandra"),("Dr. B. R. Ambedkar Station, Vidhana Soudha","Dr. B. R. Ambedkar Station, Vidhana Soudha"),("Garudacharapalya","Garudacharapalya"),("Goraguntepalya","Goraguntepalya"),("Halasuru","Halasuru"),("Hoodi","Hoodi"),("Hopefarm Channasandra","Hopefarm Channasandra"),("Indiranagar","Indiranagar"),("Jalahalli","Jalahalli"),("Jayanagar","Jayanagar"),("Jayaprakash Nagar","Jayaprakash Nagar"),("Jnanabharathi","Jnanabharathi"),("Kadugodi Tree Park","Kadugodi Tree Park"),("Kengeri","Kengeri"),("Kengeri Bus Terminal","Kengeri Bus Terminal"),("Konanakunte Cross","Konanakunte Cross"),("Krantivira Sangolli Rayanna Railway Station","Krantivira Sangolli Rayanna Railway Station"),("Krishna Rajendra Market","Krishna Rajendra Market"),("Krishnarajapura (K.R.Pura)","Krishnarajapura (K.R.Pura)"),("Kundalahalli","Kundalahalli"),("Lalbagh","Lalbagh"),("Magadi Road","Magadi Road"),("Mahakavi Kuvempu Road","Mahakavi Kuvempu Road"),("Mahalakshmi","Mahalakshmi"),("Mahatma Gandhi Road","Mahatma Gandhi Road"),("Mantri Square Sampige Road","Mantri Square Sampige Road"),("Mysore Road","Mysore Road"),("Nadaprabhu Kempegowda Station, Majestic","Nadaprabhu Kempegowda Station, Majestic"),("Nagasandra","Nagasandra"),("Nallurhalli","Nallurhalli"),("National College","National College"),("Pantharapalya - Nayandahalli","Pantharapalya - Nayandahalli"),("Pattanagere","Pattanagere"),("Pattandur Agrahara","Pattandur Agrahara"),("Peenya","Peenya"),("Peenya Industry","Peenya Industry"),("Rajajinagar","Rajajinagar"),("Rajarajeshwari Nagar","Rajarajeshwari Nagar"),("Rashtreeya Vidyalaya Road","Rashtreeya Vidyalaya Road"),("Sandal Soap Factory","Sandal Soap Factory"),("Seetharampalya","Seetharampalya"),("Silk Institute","Silk Institute"),("Singayyanapalya","Singayyanapalya"),("Sir.M.Visvesvaraya Stn., Central College","Sir.M.Visvesvaraya Stn., Central College"),("South End Circle","South End Circle"),("Sri Balagangadharanatha Swamiji Station, Hosahalli","Sri Balagangadharanatha Swamiji Station, Hosahalli"),("Sri Sathya Sai Hospital","Sri Sathya Sai Hospital"),("Srirampura","Srirampura"),("Swami Vivekananda Road","Swami Vivekananda Road"),("Thalaghattapura","Thalaghattapura"),("Trinity","Trinity"),("Vajarahalli","Vajarahalli"),("Vijayanagar","Vijayanagar"),("Whitefield (Kadugodi)","Whitefield (Kadugodi)"),("Yelachenahalli","Yelachenahalli"),("Yeshwanthpur","Yeshwanthpur")])
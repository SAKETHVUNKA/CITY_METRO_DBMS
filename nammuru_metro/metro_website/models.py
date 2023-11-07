from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, phone=''):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, phone=''):
        user = self.create_user(username, password, phone)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


stationMappings = {
    "Attiguppe":"AGPP","Baiyappanahalli":"BYPL","Banashankari":"BSNK","Benniganahalli":"BENN","Challaghatta":"CHAL","Chickpete":"CKPE","Cubbon Park":"CBPK","Dasarahalli":"DSH","Deepanjali Nagar":"DJNR","Doddakallasandra":"KLPK","Dr. B. R. Ambedkar Station, Vidhana Soudha":"VDSA","Garudacharapalya":"GDCP","Goraguntepalya":"YPI","Halasuru":"HLRU","Hoodi":"DKIA","Hopefarm Channasandra":"UWVL","Indiranagar":"IDN","Jalahalli":"JLHL","Jayanagar":" JYN","Jayaprakash Nagar":"JPN","Jnanabharathi":"BGUC","Kadugodi Tree Park":"KDGD","Kengeri":"KGIT","Kengeri Bus Terminal":"MLSD","Konanakunte Cross":"APRC","Krantivira Sangolli Rayanna Railway Station":"SRCS","Krishna Rajendra Market":"KRMT","Krishnarajapura (K.R.Pura)":"KRAM","Kundalahalli":"KDNH","Lalbagh":"LBGH","Magadi Road":"MIRD","Mahakavi Kuvempu Road":"KVPR","Mahalakshmi":"MHLI","Mahatma Gandhi Road":"MAGR","Mantri Square Sampige Road":"SPGD","Mysore Road":"MYRD","Nadaprabhu Kempegowda Station, Majestic":"KGWA","Nagasandra":"NGSA","Nallurhalli":"VDHP","National College":"NLC","Pantharapalya - Nayandahalli":"NYHM","Pattanagere":"PATG","Pattandur Agrahara":"ITPL","Peenya":"PEYA","Peenya Industry":"PYID","Rajajinagar":"RJNR","Rajarajeshwari Nagar":"RRRN","Rashtreeya Vidyalaya Road":"RVR","Sandal Soap Factory":"SSFY","Seetharampalya":"VWIA","Silk Institute":"APTS","Singayyanapalya":"MDVP","Sir.M.Visvesvaraya Stn., Central College":"VSWA","South End Circle":"SECE","Sri Balagangadharanatha Swamiji Station, Hosahalli":"HSLI","Sri Sathya Sai Hospital":"SSHP","Srirampura":"SPRU","Swami Vivekananda Road":"SVRD","Thalaghattapura":"TGTP","Trinity":"TTY","Vajarahalli":"VJRH","Vijayanagar":"VJN","Whitefield (Kadugodi)":"WHTM","Yelachenahalli":"PUTH","Yeshwanthpur":"YPM"
}

stationReverseMappings = {
    'AGPP': 'Attiguppe',
    'BYPL': 'Baiyappanahalli',
    'BSNK': 'Banashankari',
    'BENN': 'Benniganahalli',
    'CHAL': 'Challaghatta',
    'CKPE': 'Chickpete',
    'CBPK': 'Cubbon Park',
    'DSH': 'Dasarahalli',
    'DJNR': 'Deepanjali Nagar',
    'KLPK': 'Doddakallasandra',
    'VDSA': 'Dr. B. R. Ambedkar Station, Vidhana Soudha',
    'GDCP': 'Garudacharapalya',
    'YPI': 'Goraguntepalya',
    'HLRU': 'Halasuru',
    'DKIA': 'Hoodi',
    'UWVL': 'Hopefarm Channasandra',
    'IDN': 'Indiranagar',
    'JLHL': 'Jalahalli',
    ' JYN': 'Jayanagar',
    'JPN': 'Jayaprakash Nagar',
    'BGUC': 'Jnanabharathi',
    'KDGD': 'Kadugodi Tree Park',
    'KGIT': 'Kengeri',
    'MLSD': 'Kengeri Bus Terminal',
    'APRC': 'Konanakunte Cross',
    'SRCS': 'Krantivira Sangolli Rayanna Railway Station',
    'KRMT': 'Krishna Rajendra Market',
    'KRAM': 'Krishnarajapura (K.R.Pura)',
    'KDNH': 'Kundalahalli',
    'LBGH': 'Lalbagh',
    'MIRD': 'Magadi Road',
    'KVPR': 'Mahakavi Kuvempu Road',
    'MHLI': 'Mahalakshmi',
    'MAGR': 'Mahatma Gandhi Road',
    'SPGD': 'Mantri Square Sampige Road',
    'MYRD': 'Mysore Road',
    'KGWA': 'Nadaprabhu Kempegowda Station, Majestic',
    'NGSA': 'Nagasandra',
    'VDHP': 'Nallurhalli',
    'NLC': 'National College',
    'NYHM': 'Pantharapalya - Nayandahalli',
    'PATG': 'Pattanagere',
    'ITPL': 'Pattandur Agrahara',
    'PEYA': 'Peenya',
    'PYID': 'Peenya Industry',
    'RJNR': 'Rajajinagar',
    'RRRN': 'Rajarajeshwari Nagar',
    'RVR': 'Rashtreeya Vidyalaya Road',
    'SSFY': 'Sandal Soap Factory',
    'VWIA': 'Seetharampalya',
    'APTS': 'Silk Institute',
    'MDVP': 'Singayyanapalya',
    'VSWA': 'Sir.M.Visvesvaraya Stn., Central College',
    'SECE': 'South End Circle',
    'HSLI': 'Sri Balagangadharanatha Swamiji Station, Hosahalli',
    'SSHP': 'Sri Sathya Sai Hospital',
    'SPRU': 'Srirampura',
    'SVRD': 'Swami Vivekananda Road',
    'TGTP': 'Thalaghattapura',
    'TTY': 'Trinity',
    'VJRH': 'Vajarahalli',
    'VJN': 'Vijayanagar',
    'WHTM': 'Whitefield (Kadugodi)',
    'PUTH': 'Yelachenahalli',
    'YPM': 'Yeshwanthpur'
}
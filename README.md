# Şirin Anlar — Ev Şirniyyatları Saytı

Django əsasında qurulmuş, əl ilə hazırlanan tortlar, pirojnalar və ev
şirniyyatları satan kiçik bir mağaza saytı. Kateqoriyalara bölünmüş menyu,
axtarış/filtr imkanı, məhsul detalları və canlı chat formatında əlaqə
bölməsi daxildir.

## Xüsusiyyətlər

- **Menyu və kateqoriyalar** — məhsullar kateqoriyaya görə süzülür, ad və
  təsvirə görə axtarılır, nəticələr səhifələnir (pagination).
- **Məhsul detalı** — hər məhsulun öz səhifəsi, stok vəziyyəti və bənzər
  məhsul tövsiyələri.
- **Əlaqə / sifariş** — chat formatında mesajlaşma paneli; ad, telefon və
  mesaj sahələri server tərəfində doğrulanır (validasiya), nəticə istifadəçiyə
  səhifə yenilənmədən (AJAX) göstərilir.
- **Admin panel** — `/admin/` ünvanından kateqoriya, məhsul (şəkil, stok,
  qiymət) və gələn mesajları idarə etmək mümkündür.
- **Responsiv dizayn** — mobil, planşet və masaüstü üçün tam uyğunlaşdırılıb.
- **Performans** — tez-tez süzülən sahələr (`is_available`, `is_featured`)
  üzərində verilənlər bazası indeksi; admin panel siyahılarında N+1 sorğu
  problemi `select_related` ilə aradan qaldırılıb.

## Texnologiyalar

- Python / Django
- SQLite (lokal inkişaf üçün)
- **Tailwind CSS** (utility-first CSS) — hazır kompilyasiya olunmuş fayl
  (`shop/static/shop/css/style.css`) layihəyə daxildir, saytı işə salmaq üçün
  Node.js **tələb olunmur**. Node.js yalnız dizaynı dəyişmək istəsəniz lazımdır
  (aşağıya bax).
- **Alpine.js** (CDN) — mobil menyu, toast bildirişlər, yuxarı qayıt düyməsi
  və scroll animasiyaları üçün yüngül reaktivlik.

## Qurulum (sayt üçün — Django)

```bash
# 1) Virtual mühit yaradın və aktivləşdirin
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2) Asılılıqları quraşdırın
pip install -r requirements.txt

# 3) Verilənlər bazası cədvəllərini yaradın
python manage.py migrate

# 4) Admin panelə giriş üçün istifadəçi yaradın
python manage.py createsuperuser

# 5) Serveri işə salın
python manage.py runserver
```

Sayt: <http://127.0.0.1:8000/>
Admin panel: <http://127.0.0.1:8000/admin/>

Admin paneldən ilk kateqoriya və məhsulları əlavə etməklə sayt dərhal
işlək hala gələcək.

## Dizaynı dəyişmək (Tailwind CSS) — istəyə bağlı

CSS `shop/static/shop/css/input.css` faylından **kompilyasiya olunur**.
Yəni birbaşa `style.css`-i əl ilə redaktə etməyin — dəyişiklik növbəti
kompilyasiyada silinər. Rəng, şrift və s. `tailwind.config.js`-də,
təkrarlanan komponent stilləri (`.btn`, `.card`, `.chat-bubble` və s.)
isə `input.css`-də (`@layer components` daxilində) saxlanılır.

```bash
# Yalnız bir dəfə: Node.js paketlərini quraşdırın
npm install

# HTML şablonlarını dəyişdikcə CSS-i canlı yeniləmək üçün (inkişaf zamanı)
npm run watch

# Son, kiçildilmiş (minified) CSS-i yaratmaq üçün (təhvil verməzdən əvvəl)
npm run build
```

Node.js quraşdırılmayıbsa: <https://nodejs.org> ünvanından LTS versiyasını
yükləyin (`npm` onunla birlikdə gəlir).

## Vercel-ə deployment

Layihə Vercel-in serverless Python funksiyaları üzərində işləyəcək şəkildə
konfiqurasiya edilib. Lokalda SQLite, Vercel-də isə `DATABASE_URL` mühit
dəyişəni verildikdə avtomatik olaraq PostgreSQL istifadə olunur — heç bir
kod dəyişikliyi tələb olunmur.

**Addımlar:**

1. Layihəni GitHub-a push edin.
2. Vercel-də "New Project" edib repo-nu qoşun.
3. Bir PostgreSQL bazası əlavə edin (Vercel Postgres, Neon və ya Supabase —
   hər hansı birindən `DATABASE_URL` (və ya `POSTGRES_URL`) dəyişənini
   götürün).
4. Vercel Project → Settings → Environment Variables bölməsində bunları əlavə edin:

   | Dəyişən | Dəyər |
   |---|---|
   | `DATABASE_URL` | PostgreSQL bağlantı ünvanınız |
   | `DJANGO_SECRET_KEY` | Təsadüfi, gizli açar |
   | `DJANGO_DEBUG` | `0` |
   | `DJANGO_ALLOWED_HOSTS` | `.vercel.app` (və ya öz domeniniz) |

5. Bazanı Vercel-ə qoşmazdan əvvəl, öz kompüterinizdən miqrasiyaları icra edin:

   ```bash
   DATABASE_URL="Vercel-dən aldığınız ünvan" python manage.py migrate
   DATABASE_URL="Vercel-dən aldığınız ünvan" python manage.py createsuperuser
   ```

6. Statik faylları yenidən topladıqdan sonra commit edin (bu, WhiteNoise-un
   Vercel üzərində CSS/JS fayllarını tapması üçün lazımdır):

   ```bash
   python manage.py collectstatic --noinput
   git add staticfiles
   git commit -m "Statik faylları yenilə"
   ```

7. Deploy edin.

**Bilinən məhdudiyyət:** Vercel-in serverless mühiti fayl sisteminə daimi
yazma icazəsi vermir. Bu o deməkdir ki, admin paneldən **məhsul şəkli
yükləmək** production-da (Vercel-də) işləməyəcək — yüklənən fayl bir sonrakı
sorğuda itəcək. Bunu həll etmək üçün xarici saxlama xidməti (məsələn,
Cloudinary, AWS S3 və ya Vercel Blob) qoşmaq lazımdır. İstəsəniz bunu da
əlavə edə bilərəm — hazırda şəkilləri yalnız lokal inkişaf mühitində
yükləmək tövsiyə olunur.

## Layihə strukturu

```
sirin_anlar/
├── manage.py
├── requirements.txt
├── vercel.json              # Vercel deployment konfiqurasiyası
├── .vercelignore
├── api/
│   └── index.py             # Vercel serverless giriş nöqtəsi (WSGI)
├── package.json            # Tailwind build skriptləri (build / watch)
├── tailwind.config.js       # Rəng palitrası, şrift, kölgə tənzimləmələri
├── sirin_anlar/            # Layihənin əsas konfiqurasiyası
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
└── shop/                   # Əsas tətbiq (app)
    ├── models.py           # Category, Product, ContactMessage
    ├── views.py            # Səhifə məntiqi
    ├── forms.py            # Əlaqə/sifariş formu
    ├── admin.py            # Admin panel tənzimləmələri
    ├── urls.py              # shop app-in route-ları
    ├── migrations/
    ├── templates/shop/     # HTML şablonları (Tailwind class-ları ilə)
    └── static/shop/css/
        ├── input.css        # Tailwind mənbə fayl (bunu redaktə edin)
        └── style.css         # Kompilyasiya olunmuş, hazır fayl (avtomatik yaranır)
```

## Mühit dəyişənləri (production üçün)

Lokal işlədərkən heç nə tənzimləməyə ehtiyac yoxdur — bütün parametrlərin
məqul standart (default) dəyəri var. Serverə yerləşdirərkən aşağıdakıları
təyin etmək tövsiyə olunur:

| Dəyişən                | Təyinatı                                              |
|-------------------------|--------------------------------------------------------|
| `DJANGO_SECRET_KEY`     | Təsadüfi, gizli bir açar                               |
| `DJANGO_DEBUG`          | Production-da `0` olmalıdır                            |
| `DJANGO_ALLOWED_HOSTS`  | Domen adları, vergüllə ayrılmış (məs: `sirinanlar.az`) |
| `DATABASE_URL`          | Verilsə, PostgreSQL istifadə olunur; verilməsə SQLite  |

## Qeyd

`db.sqlite3` və `media/` qovluğu `.gitignore`-a əlavə olunub — bunlar hər
mühitdə fərqli ola biləcəyi üçün versiya nəzarətinə daxil edilmir.
`staticfiles/` isə Vercel deploymenti üçün **bilərəkdən** commit olunur
(yuxarıdakı "Vercel-ə deployment" bölməsinə baxın). Onu yenidən yaratmaq
üçün:

```bash
python manage.py collectstatic
```

# Project-4 

<h2>Overview</h2>

<p>My final GA project was a solo venture, developed with a Python Django back-end and React front-end. I decided on Dinosaur PetShop - an online pet store where you could browse for and ‘buy’ different species of dinosaur, as well as related food and toys.</p>

<a href="">Visit Dinosaur Petshop here.</a>

<a href="https://github.com/tdore92/project-4-client">Client Repository</a>

<h2>Brief</h2>

<li>Build a full-stack application by making your own backend and your own front-end.</li>
<li>Use a Python Django API using Django REST Framework to serve your data from a Postgres database.</li>
<li>Consume your API with a separate front-end built with React.</li>
<li>Be a complete product which most likely means multiple relationships and CRUD functionality for at least a couple of models.</li>
<li>Implement thoughtful user stories/wireframes that are significant enough to help you know which features are core MVP and which you can cut.</li>
<li>Have a visually impressive design to kick your portfolio up a notch and have something to wow future clients & employers. ALLOW time for this.</li>
<li>Be deployed online so it's publicly accessible.</li>


<h2>Technologies Used</h2>

<li>Python</li>
<li>React</li>
<li>Django</li>
<li>Postgres</li>
<li>Git</li>
<li>Github</li>
<li>Bulma</li>
<li>Material-UI</li>

<h2>Approach Taken</h2>

<p>To begin with I pseudo-coded the pages and features I wanted to include. Given the deadline, my recent exposure to Python and the fact it would be a solo venture I opted to keep it fairly simple to start with - home, index and show pages, with a ‘basket’ page similar to what my team and I attempted in project 2.</p>

<img src="https://i.imgur.com/HMD4rXz.png" alt="DPS Pseudo"/> 

<h3>Backend</h3>

<p>I built my two models - Dinosaurs and Misc. The reasoning behind this was to give each model a different set of classes that could be accessed in various ways in React.</p>

```
class Dinosaur(models.Model):
    name = models.CharField(max_length=50)

    class Type(models.TextChoices):
        CARNIVORE = 'Carnivore', _('Carnivore')
        HERBIVORE = 'Herbivore', _('Herbivore')
        PISCIVORE = 'Piscivore', _('Piscivore')

    type = models.CharField (
        max_length= 10,
        choices=Type.choices,
        default=Type.CARNIVORE
    )

    def is_upperclass(self):
        return self.type in {
        self.Type.CARNIVORE,
        self.Type.HERBIVORE,
    }

    danger_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  
    class Size(models.TextChoices):
        LARGE = 'Large', _('Large')
        MEDIUM = 'Medium', _('Medium')
        SMALL = 'Small', _('Small')

    size = models.CharField (
        max_length= 10,
        choices=Size.choices,
        default=Size.MEDIUM
    )

    def is_upperclass(self):
        return self.size in {
        self.Size.MEDIUM,
        self.Size.LARGE,
        }

    description = models.CharField(max_length=500)
    image = models.CharField(max_length=250)
    price = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])

```

```
class Misc(models.Model):
    name = models.CharField(max_length=50)

# MISC TYPE CLASS

    class Misctype(models.TextChoices):
        FOOD = 'Food', _('Food')
        TOY = 'Toy', _('Toy')

    misctype = models.CharField (
        max_length= 10,
        choices=Misctype.choices,
        default=Misctype.FOOD
    )

    def is_upperclass(self):
        return self.misctype in {
        self.Misctype.FOOD,
        self.Misctype.TOY,
        }

# DINO TYPE CLASS

    class Dinotype(models.TextChoices):
        CARNIVORE = 'Carnivore', _('Carnivore')
        HERBIVORE = 'Herbivore', _('Herbivore')
        PISCIVORE = 'Piscivore', _('Piscivore')

    dinotype = models.CharField (
        max_length= 10,
        choices=Dinotype.choices,
        default=Dinotype.CARNIVORE
    )

    def is_upperclass(self):
        return self.dinotype in {
        self.Dinotype.CARNIVORE,
        self.Dinotype.HERBIVORE,
        }

# SIZE CLASS

    class Size(models.TextChoices):
        LARGE = 'Large', _('Large')
        MEDIUM = 'Medium', _('Medium')
        SMALL = 'Small', _('Small')

    size = models.CharField (
        max_length= 10,
        choices=Size.choices,
        default=Size.MEDIUM
    )

    def is_upperclass(self):
            return self.size in {
            self.Size.MEDIUM,
            self.Size.LARGE,
            }

# DESCRIP, IMAGE AND PRICE

    description = models.CharField(max_length=500)
    image = models.CharField(max_length=250)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

```

<p>I then used Django Admin to quickly add some data sets.</p>

<p><strong>Update:</strong> Whilst building the frontend I discovered having two separate models created more problems than it solved - particularly when it came to combining selected data sets in the 'basket' page. To fix this and streamline the backend functionality in general, I removed the existing user models and created a single 'items' model that combined classes from the 'dinosaur' and 'misc' models.</p>

```
class Item(models.Model):

    name = models.CharField(max_length=50)

    type = models.CharField(max_length=50)

    diet = models.CharField(max_length=50)

    size = models.CharField(max_length=50)

    description = models.CharField(max_length=500)

    price = models.FloatField(default=0)

    image = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'

```

<p>The models that previously required a text_choices value were changed to hold a charField value, so CRUD-based forms were simpler to execute in the frontend.</p>

<p>Once the items model was functional, I created an additional user model, login and register views, and token authentication.</p>

```
class User(AbstractUser):
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250)
```
```
User = get_user_model()

class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header:
            return None
        if not header.startswith('Bearer'):
            raise PermissionDenied({'detail': 'Invalid Authorization Header'})

        token = header.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload.get('sub'))
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied({'detail': 'Invalid Token'})
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'User Not Found'})

        return (user, token)
```
```
class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'detail': 'Unauthorized'})

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id, 'exp': int(expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response(
            {'token': token, 'message': f'Welcome back {user_to_login.username}'}
            )
```

<h3>Frontend</h3>

<p>The index and show pages came together swiftly - on the home page, I opted for a simplistic, bulma-styled design.</p>

<img src="https://i.imgur.com/6QsUY2I.png" alt="DPS Home"/>

<p><strong>Update:</strong> Upon a successful login, the users navbar now changes to reveal a 'post your dinosaur' option, and replaces the 'login/register' options with a 'log out' variant.</p>

```
{!isLoggedIn ?
                <>
                </>
                :
                <>
                  <Link to="/dinosaurs/new" className="has-text-black">Post Your Dinosaur</Link>
                </>
              }
```
```
            {!isLoggedIn ?
              <>
                <div className="navbar-item">
                  <Link to="/Register" className="has-text-black">Register</Link>
                </div>
                <div className="navbar-item">
                  <Link to="/Login" className="has-text-black">Login</Link>
                </div>

              </>
              :
              <>

                <div className="navbar-item">
                  <p className="has-text-black" onClick={handleLogout}>Log Out</p>
                </div>
              </>

            }
```

<p>The basket page followed the same idea that my colleague and I attempted in project 2 - take an item, push it into a new array and then map it out on the desired page. Here, I found setting state solved our previous issue, and the desired items would now be displayed in the basket.</p>

```
const handleClick = (e) => {
    console.log(e.target.value)
    const basketItem = JSON.parse(window.localStorage.getItem('dinos')) || []
    console.log(dino)
    basketItemArray = [...basketItemArray, dino]
    basketItem.push(dino)
    localStorage.setItem('dinos', JSON.stringify(basketItem))
    console.log(basketItemArray)
    history.push('/dinosaurs')
```
```
const [basketItems, setBasketItems] = React.useState(() => JSON.parse(window.localStorage.getItem('dinos')))

```

<p>From here I added a ‘Total’ counter that displayed the combined items price, and a ‘Remove Item’ button that would affect the counter in return. I installed ‘Material-UI’ and used their button components to create a basic ‘checkout’ button.</p>

<p><strong>Update:</strong> I later applied 'Material-UI' to the show page - when the 'add to basket' button is clicked, the user is notified of the said item being added, instead of being pushed to the home page.</p>

```
const totalDinoPrice = basketItems.reduce((runningTotal, item) => {
    return runningTotal + item.price
  }, 0)

  const totalMiscPrice = basketMiscItems.reduce((runningTotal, item) => {
    return runningTotal + item.price
    
  }, 0)

```

```
const handleDelete = (e) => {
    const newBasketItems = basketItems.filter((_, index) => index !== Number(e.target.value))
    localStorage.setItem('dinos', JSON.stringify(newBasketItems))
    setBasketItems(newBasketItems)
  }

  const handleMiscsDelete = (e) => {
    const newBasketItems = basketMiscItems.filter((_, index) => index !== Number(e.target.value))
    localStorage.setItem('miscs', JSON.stringify(newBasketItems))
    setBasketItems(newBasketItems)
  }

```

<p>There being two arrays, two counters and remove buttons were made - the deadline on the horizon, I’ve opted to come back to the resulting bugs later on, either to spread and combine the two arrays or refactor my code entirely.</p>

<p><strong>Update:</strong> The backend refactoring meant this process could now be simplified. Instead of handling two arrays, there is only one basket array to map and filter, thus only one handleDelete function needed.</p>

<img src="https://i.imgur.com/ywp71ZZ.png" alt="Basket page"/>

<h2>Wins</h2>

<p>Basket: In project 2 my team and I tried to create a similar feature that we didn't quite figure out how to implement in time, so it felt quite satisfying to succeed in a solo venture this time around.</p>

<p>Refactoring: The deadline having passed, I wasn't satisfied with the end result. It's felt very rewarding to come back to this project and refactor and refine certain elements, and I'm looking to tinker with it further.</p>

<h2>Challenges</h2>

<p>Grappling with two separate models when creating the Basket and Related Product features brought more complex logic to the table than was required. Whilst I came up with a solution to the Basket component it's something I'm keen to go back to and rectify in the next few weeks.</p>

<h2>Bugs</h2>

<li>Image upload functionality to be fixed.</li>
<li>401 error when Registering new user in Django.</li>
<li>Delete function in Basket occasionally requires refreshing the page for changes to take effect.</li>

<h2>Future Features</h2>

<li>Q&A page that recommends a dinosaur for you.</li>
<li>A 'related products' section for the show page of each dinosaur.</li>

<h2>Lessons learned</h2>

<li>Come the deadline, I had far more bugs than I would have liked. Many of them came from mistakes made in my planning, particularly my decision to use two models whereby one would have sufficed. The solution would be to utilise a single model with expanded classes, which would reduce the problem solving required in the basket & related product apps especially. In short, Keep It Simple Stupid!</li>
<br/>
<p><small>NOTE: This Readme will be updated over time as the bug fixes and outstanding features are implemented.</small></p>
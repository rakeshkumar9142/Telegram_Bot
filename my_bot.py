import logging
import os
import httpx
import random
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationHandlerStop

# --- Web Server Setup (for Render's Free Tier) ---

app = Flask(__name__)

@app.route('/')
def hello():
    return "Bot is alive!"

def run_flask_app():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- Telegram Bot Configuration ---

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# IMPORTANT: Replace these with env vars in production
TOKEN = os.getenv("TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

COMMANDS = {
    "start": "🚀 Start the bot",
    "news": "📰 Get news on a topic",
    "about": "🌍 Learn about OpenStart",
    "quote": "💡 Get a motivational quote",
    "help": "❓ See this list of commands",
    "team": "👥 Meet the OpenStart team",
    "events": "📅 See upcoming events",
    "mentor": "🎓 Learn about mentorship",
    "resources": "📚 Access learning materials",
    "faq": "❔ Frequently Asked Questions",
    "apply": "📝 How to apply for programs",
    "contact": "📩 Get in touch with the team",
    "feedback": "💬 Share your feedback with us",
    "community": "🌐 Join our global community",
}

# --- Command Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        f"Hi {user.first_name}! 👋\n\n"
        "Welcome to the **OpenStart Project Bot**!\n\n"
        "I'm your assistant for all things related to startups, funding, and innovation for young founders. "
        "What would you like to do first?"
    )
    keyboard = [
        [KeyboardButton("/news funding"), KeyboardButton("/quote")],
        [KeyboardButton("/team"), KeyboardButton("/help")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Here's the full list of what I can do for you:\n\n"
    for command, description in COMMANDS.items():
        help_text += f"/{command} - {description}\n"
    await update.message.reply_text(help_text)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "**🌍 About OpenStart**\n\n"
        "OpenStart is a global accelerator program for **high school students**. "
        "Our mission is to connect ambitious young minds with world-class mentorship, resources, and opportunities to build real, meaningful projects."
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "startup"
    await update.message.reply_text(f"🔍 Searching for the latest news about '{topic}'...")

    url = f"https://newsapi.org/v2/everything?q={topic}&searchIn=title&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                await update.message.reply_text(f"Sorry, I couldn't find any recent news for '{topic}'.")
                return

            news_message = f"**Top 5 News Articles for '{topic.title()}'**\n\n"
            for article in articles:
                news_message += f"▪️ [{article['title']}]({article['url']})\n\n"

            await update.message.reply_text(news_message, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        logging.error(f"News command error: {e}")
        await update.message.reply_text("Sorry, an error occurred while fetching news.")


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "The best way to predict the future is to create it. - Peter Drucker",
        "Your most unhappy customers are your greatest source of learning. - Bill Gates",
        "It’s not about ideas. It’s about making ideas happen. - Scott Belsky",
        "A goal is a dream with a deadline. - Napoleon Hill",
"A goal properly set is halfway reached. - Zig Ziglar",
"A good conscience is a continual Christmas. - Benjamin Franklin",
"A guaranteed way to be miserable is to spend all your time trying to make everyone else happy. - Larry Winget",
"A man wrapped up in himself makes a very small bundle. - Benjamin Franklin",
"A mediocre idea that generates enthusiasm will go further than a great idea that inspires no one. - Mary Kay Ash",
"A strong foundation at home sets you up for a strong foundation at work. - Robin Sharma",
"Accept the challenges so you can feel the exhilaration of victory. - George S. Patton",
"Accept your teammates for what they are and inspire them to become all they can be. - Robin Sharma",
"Act as if what you do makes a difference. It does. - William James",
"Action is the foundational key to all success. - Pablo Picasso",
"Aim for the moon. If you miss you may hit a star. - W. Clement Stone",
"All great thinkers are initially ridiculed – and eventually revered. - Robin Sharma",
"All of your dreams await just on the other side of your fears. - Grant Cardone",
"Always choose the future over the past. What do we do now? - Brian Tracy",
"Always do your best. What you plant now, you will harvest later. - Og Mandino",
"Always give without remembering and always receive without forgetting. - Brian Tracy",
"Amateurs sit and wait for inspiration, the rest of us just get up and go to work. - Stephen King",
"An attitude of a positive expectation is the mark of the superior personality. - Brian Tracy",
"Anger is never without a reason, but seldom with a good one. - Benjamin Franklin",
"Any fool can criticize, condemn and complain - and most fools do. - Benjamin Franklin",
"Any thought or action that you repeat over and over will eventually become a new habit. - Brian Tracy",
"Arriving at one goal is the starting point to another. - John Dewey",
"As we each express our natural genius, we all elevate our world. - Robin Sharma",
"Be gentle to all and stern with yourself. - Saint Teresa of Avila",
"Be kind whenever possible. It is always possible. - Dalai Lama",
"Be miserable. Or motivate yourself. Whatever has to be done, it's always your choice. - Wayne Dyer",
"Become a person who would attract the results you seek. - Jim Cathcart",
"Before you begin scrambling up the ladder of success, make sure that it is leaning against the right building. - Brian Tracy",
"Being the richest man in the cemetery doesn't matter to me. Going to bed at night saying we've done something wonderful, that's what matters to me. - Steve Jobs",
"Belief triggers the power to do. - David J. Schwartz",
"Believe you can and you're halfway there. - Theodore Roosevelt",
"Big shots are only little shots who keep shooting. - Christopher Morley",
"Business is like riding a bicycle. Either you keep moving or you fall down. - Frank Lloyd Wright",
"By failing to prepare, you are preparing to fail. - Benjamin Franklin",
"Change is hardest at the beginning, messiest in the middle and best at the end. - Robin Sharma",
"Clarity precedes mastery. Craft clear and precise plans/goals/deliverables. And then block out all else. - Robin Sharma",
"Courage is not absence of fear; it is control of fear, mastery of fear. - Mark Twain",
"Crush your fears with ACTION. - Russell Frazier",
"Daily exercise is an insurance policy against future illness. The best Leaders Without Titles are the fittest. - Robin Sharma",
"Deserve your dream. - Octavio Paz",
"Discipline is the bridge between goals and accomplishment. - Jim Rohn",
"Discipline is what you must have to resist the lure of excuses. - Brian Tracy",
"Do not let what you cannot do interfere with what you can do. - John Wooden",
"Do or do not. There is no try. - Yoda",
"Do something wonderful, people may imitate it. - Albert Schweitzer",
"Do the difficult things while they are easy and do the great things while they are small. A journey of a thousand miles must begin with a single step. - Lao Tzu",
"Do what you can, with what you have, where you are. - Theodore Roosevelt",
"Doing the best at this moment puts you in the best place for the next moment. - Oprah Winfrey",
"Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
"Don't be pushed by your problems; be led by your dreams. - Unknown",
"Don't let what you cannot do interfere with what you can do. - John Wooden",
"Don't spend time beating on a wall, hoping to transform it into a door. - Coco Chanel",
"Dream big and dare to fail. - Norman Vaughan",
"Dreams are today's answers to tomorrow's questions. - Edgar Cayce",
"Eighty percent of success is showing up. - Woody Allen",
"Even if you're on the right track, you'll get run over if you just sit there. - Will Rogers",
"Every child is an artist. The problem is how to remain an artist once he grows up. - Pablo Picasso",
"Every day is a new beginning, take a deep breath and start again. - Unknown",
"Every strike brings me closer to the next home run. - Babe Ruth",
"Everything has beauty, but not everyone can see. - Confucius",
"Everything that irritates us about others can lead us to an understanding of ourselves. - Carl Jung",
"Everything you’ve ever wanted is on the other side of fear. - George Addair",
"Experience is the teacher of all things. - Julius Caesar",
"Fall seven times and stand up eight. - Japanese Proverb",
"Fear is the disease. Hustle is the antidote. - Travis Kalanick",
"First, have a definite, clear practical ideal; a goal, an objective. Second, have the necessary means to achieve your ends; wisdom, money, materials, and methods. Third, adjust all your means to that end. - Aristotle",
"For small creatures such as we the vastness is bearable only through love. - Carl Sagan",
"Forget past mistakes. Forget failures. Forget everything except what you're going to do now and do it. - William Durant",
"From a small seed a mighty trunk may grow. - Aeschylus",
"Get out of your head and get into your heart. Think less, feel more. - Osho",
"Give me a lever long enough and a fulcrum on which to place it, and I shall move the world. - Archimedes",
"Go as far as you can see; when you get there, you'll be able to see farther. - J. P. Morgan",
"Go confidently in the direction of your dreams. Live the life you have imagined. - Henry David Thoreau",
"Goals may give focus, but dreams give power. - John Maxwell",
"Good, better, best. Never let it rest. 'Til your good is better and your better is best. - St. Jerome",
"Great acts are made up of small deeds. - Lao Tzu",
"Happiness is not something readymade. It comes from your own actions. - Dalai Lama",
"Happiness often sneaks in through a door you didn't know you left open. - John Barrymore",
"He who has health has hope; and he who has hope has everything. - Arabian Proverb",
"He who has a why to live can bear almost any how. - Friedrich Nietzsche",
"He who is not courageous enough to take risks will accomplish nothing in life. - Muhammad Ali",
"Health is the greatest gift, contentment the greatest wealth, faithfulness the best relationship. - Buddha",
"High expectations are the key to everything. - Sam Walton",
"How wonderful it is that nobody need wait a single moment before starting to improve the world. - Anne Frank",
"I am not a product of my circumstances. I am a product of my decisions. - Stephen Covey",
"I attribute my success to this: I never gave or took an excuse. - Florence Nightingale",
"I can, therefore I am. - Simone Weil",
"I didn't fail the test. I just found 100 ways to do it wrong. - Benjamin Franklin",
"I have learned over the years that when one's mind is made up, this diminishes fear. - Rosa Parks",
"I never dreamed about success, I worked for it. - Estee Lauder",
"I think I can. I know I can. - Unknown",
"I would rather die of passion than of boredom. - Vincent van Gogh",
"I'd rather attempt to do something great and fail than to attempt to do nothing and succeed. - Robert H. Schuller",
"If it scares you, it may be a good thing to try. - Seth Godin",
"If the world seems cold to you, kindle fires to warm it. - Lucy Larcom",
"If you aim at nothing, you'll hit it every time. - Unknown",
"If you are not willing to risk the usual you will have to settle for the ordinary. - Jim Rohn",
"If you can dream it, you can achieve it. - Zig Ziglar",
"If you do what you've always done, you'll get what you've always gotten. - Tony Robbins",
"If you don't like something, change it. If you can't change it, change your attitude. - Maya Angelou",
"If you don't risk anything, you risk even more. - Erica Jong",
"If you hear a voice within you say 'you cannot paint,' then by all means paint and that voice will be silenced. - Vincent Van Gogh",
"If you want to lift yourself up, lift up someone else. - Booker T. Washington",
"If you want to succeed you should strike out on new paths, rather than travel the worn paths of accepted success. - John D. Rockefeller",
"If you're offered a seat on a rocket ship, don't ask what seat! Just get on. - Sheryl Sandberg",
"Imagination is more important than knowledge. - Albert Einstein",
"In a gentle way, you can shake the world. - Mahatma Gandhi",
"In every difficulty lies opportunity. - Albert Einstein",
"In order to succeed, we must first believe that we can. - Nikos Kazantzakis",
"In the middle of difficulty lies opportunity. - Albert Einstein",
"In this life we cannot do great things. We can only do small things with great love. - Mother Teresa",
"Inspiration exists, but it must find you working. - Pablo Picasso",
"It always seems impossible until it's done. - Nelson Mandela",
"It does not matter how slowly you go as long as you do not stop. - Confucius",
"It is always the simple that produces the marvelous. - Amelia Barr",
"It is during our darkest moments that we must focus to see the light. - Aristotle",
"It is never too late to be what you might have been. - George Eliot",
"It is not what you do for your children, but what you have taught them to do for themselves, that will make them successful human beings. - Ann Landers",
"It is not where you start but how high you aim that matters for success. - Nelson Mandela",
"It’s not whether you get knocked down. It’s whether you get up again. - Vince Lombardi",
"Judge each day not by the harvest you reap but by the seeds you plant. - Robert Louis Stevenson",
"Just when the caterpillar thought the world was ending, he turned into a butterfly. - Proverb",
"Keep your eyes on the stars, and your feet on the ground. - Theodore Roosevelt",
"Leadership is the capacity to translate vision into reality. - Warren Bennis",
"Learn from the past, set vivid, detailed goals for the future, and live in the only moment of time over which you have any control: now. - Denis Waitley",
"Learning is the beginning of wealth. Learning is the beginning of health. Learning is the beginning of spirituality. Searching and learning is where the miracle process all begins. - Jim Rohn",
"Let the beauty of what you love be what you do. - Rumi",
"Let us sacrifice our today so that our children can have a better tomorrow. - A. P. J. Abdul Kalam",
"Life is 10% what happens to me and 90% of how I react to it. - Charles Swindoll",
"Life is about making an impact, not making an income. - Kevin Kruse",
"Life is not measured by the number of breaths we take, but by the moments that take our breath away. - Maya Angelou",
"Life isn't about getting and having, it's about giving and being. - Kevin Kruse",
"Life shrinks or expands in proportion to one's courage. - Anais Nin",
"Listen with curiosity. Speak with honesty. Act with integrity. The greatest problem with communication is we don’t listen to understand. We listen to reply. When we listen with curiosity, we don’t listen with the intent to reply. We listen for what’s behind the words. - Roy T. Bennett",
"Little minds are tamed and subdued by misfortune; but great minds rise above it. - Washington Irving",
"Look at the sparrows; they do not know what they will do in the next moment. Let us literally live from moment to moment. - Mahatma Gandhi",
"Lost time is never found again. - Benjamin Franklin",
"Love the life you live. Live the life you love. - Bob Marley",
"Make each day your masterpiece. - John Wooden",
"Many of life's failures are people who did not realize how close they were to success when they gave up. - Thomas A. Edison",
"Money and success don’t change people; they merely amplify what is already there. - Will Smith",
"Most of the important things in the world have been accomplished by people who have kept on trying when there seemed to be no help at all. - Dale Carnegie",
"Motivation is what gets you started. Habit is what keeps you going. - Jim Rohn",
"Move out of your comfort zone. You can only grow if you are willing to feel awkward and uncomfortable when you try something new. - Brian Tracy",
"My mission in life is not merely to survive, but to thrive; and to do so with some passion, some compassion, some humor, and some style. - Maya Angelou",
"Never complain and never explain. - Benjamin Disraeli",
"Never give up, for that is just the place and time that the tide will turn. - Harriet Beecher Stowe",
"Never, never, never give up. - Winston Churchill",
"No matter what people tell you, words and ideas can change the world. - Robin Williams",
"No one can make you feel inferior without your consent. - Eleanor Roosevelt",
"No one who achieves success does so without the help of others. The wise and confident acknowledge this help with gratitude. - Alfred North Whitehead",
"Nothing is impossible, the word itself says 'I'm possible'! - Audrey Hepburn",
"Nothing will work unless you do. - Maya Angelou",
"Ones best success comes after their greatest disappointments. - Henry Ward Beecher",
"Only I can change my life. No one can do it for me. - Carol Burnett",
"Opportunities are usually disguised as hard work, so most people don't recognize them. - Ann Landers",
"Opportunities don't happen, you create them. - Chris Grosser",
"Opportunity does not knock, it presents itself when you beat down the door. - Kyle Chandler",
"Our lives begin to end the day we become silent about things that matter. - Martin Luther King Jr.",
"People often say that motivation doesn't last. Well, neither does bathing. That's why we recommend it daily. - Zig Ziglar",
"People who are crazy enough to think they can change the world, are the ones who do. - Rob Siltanen",
"Perfection is not attainable, but if we chase perfection we can catch excellence. - Vince Lombardi",
"Practice Golden Rule management in everything you do. Manage others the way you would like to be managed. - Brian Tracy",
"Problems are not stop signs, they are guidelines. - Robert H. Schuller",
"Put your heart, mind, and soul into even your smallest acts. This is the secret of success. - Swami Sivananda",
"Quality is not an act, it is a habit. - Aristotle",
"Reach for the stars so if you fall you land on a cloud. - Kanye West",
"Real difficulties can be overcome; it is only the imaginary ones that are unconquerable. - Theodore N. Vail",
"Remember no one can make you feel inferior without your consent. - Eleanor Roosevelt",
"Set your goals high, and don't stop till you get there. - Bo Jackson",
"Setting goals is the first step in turning the invisible into the visible. - Tony Robbins",
"Small daily improvements are the key to staggering long-term results. - Unknown",
"Someone sits in the shade today because someone planted a tree a long time ago. - Warren Buffett",
"Sometimes when you innovate, you make mistakes. It is best to admit them quickly, and get on with improving your other innovations. - Steve Jobs",
"Start where you are. Use what you have. Do what you can. - Arthur Ashe",
"Strive not to be a success, but rather to be of value. - Albert Einstein",
"Success consists of getting up just one more time than you fall. - Oliver Goldsmith",
"Success is dependent on effort. - Sophocles",
"Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
"Success is the sum of small efforts - repeated day in and day out. - Robert Collier",
"Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
"Take up one idea. Make that one idea your life--think of it, dream of it, live on that idea. Let the brain, muscles, nerves, every part of your body, be full of that idea, and just leave every other idea alone. This is the way to success. - Swami Vivekananda",
"Tell me and I forget. Teach me and I remember. Involve me and I learn. - Benjamin Franklin",
"The art of living lies less in eliminating our troubles than in growing with them. - Bernard M. Baruch",
"The best preparation for tomorrow is doing your best today. - H. Jackson Brown, Jr.",
"The best revenge is massive success. - Frank Sinatra",
"The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
"The best way out is always through. - Robert Frost",
"The difference between who you are and who you want to be is what you do. - Unknown",
"The first step toward success is taken when you refuse to be a captive of the environment in which you first find yourself. - Mark Caine",
"The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
"The harder the battle the sweeter the victory. - Les Brown",
"The journey of a thousand miles begins with one step. - Lao Tzu",
"The mind is everything. What you think you become. - Buddha",
"The more man meditates upon good thoughts, the better will be his world and the world at large. - Confucius",
"The most common way people give up their power is by thinking they don't have any. - Alice Walker",
"The most difficult thing is the decision to act, the rest is merely tenacity. - Amelia Earhart",
"The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
"The only place where success comes before work is in the dictionary. - Vidal Sassoon",
"The only thing that overcomes hard luck is hard work. - Harry Golden",
"The only thing worse than being blind is having sight but no vision. - Helen Keller",
"The only way to do great work is to love what you do. - Steve Jobs",
"The person who says it cannot be done should not interrupt the person who is doing it. - Chinese Proverb",
"The real test is not whether you avoid this failure, because you won't. It's whether you let it harden or shame you into inaction, or whether you learn from it; whether you choose to persevere. - Barack Obama",
"The road to success and the road to failure are almost exactly the same. - Colin R. Davis",
"The secret of joy in work is contained in one word - excellence. To know how to do something well is to enjoy it. - Pearl Buck",
"The secret of success is to do the common thing uncommonly well. - John D. Rockefeller Jr.",
"The starting point of all achievement is desire. - Napoleon Hill",
"The successful warrior is the average man, with laser-like focus. - Bruce Lee",
"The way to get started is to quit talking and begin doing. - Walt Disney",
"The whole secret of a successful life is to find out what is one's destiny to do, and then do it. - Henry Ford",
"There are no limits to what you can accomplish, except the limits you place on your own thinking. - Brian Tracy",
"There are no secrets to success. It is the result of preparation, hard work, and learning from failure. - Colin Powell",
"There is no passion to be found playing small - in settling for a life that is less than the one you are capable of living. - Nelson Mandela",
"There is only one way to avoid criticism: do nothing, say nothing, and be nothing. - Aristotle",
"There's a way to do it better - find it. - Thomas A. Edison",
"Things work out best for those who make the best of how things work out. - John Wooden",
"Think with your whole body. - Taisen Deshimaru",
"Those who say it can not be done, should not interrupt those doing it. - Chinese Proverb",
"Though no one can go back and make a brand new start, anyone can start from now and make a brand new ending. - Carl Bard",
"To accomplish great things, we must not only act, but also dream, not only plan, but also believe. - Anatole France",
"To know how much there is to know is the beginning of learning to live. - Dorothy West",
"To succeed in life, you need two things: ignorance and confidence. - Mark Twain",
"Today’s accomplishments were yesterday’s impossibilities. - Robert H. Schuller",
"Too many of us are not living our dreams because we are living our fears. - Les Brown",
"Try not to become a man of success. Rather become a man of value. - Albert Einstein",
"Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails. Explore, Dream, Discover. - Mark Twain",
"Two roads diverged in a wood, and I took the one less traveled by, and that has made all the difference. - Robert Frost",
"We all have ability. The difference is how we use it. - Stevie Wonder",
"We become what we think about. - Earl Nightingale",
"We can do anything we want to if we stick to it long enough. - Helen Keller",
"We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light. - Plato",
"We can't help everyone, but everyone can help someone. - Ronald Reagan",
"We generate fears while we sit. We overcome them by action. - Dr. Henry Link",
"We must believe that we are gifted for something, and that this thing, at whatever cost, must be attained. - Marie Curie",
"Weak people revenge. Strong people forgive. Intelligent people ignore. - Albert Einstein",
"What seems to us as bitter trials are often blessings in disguise. - Oscar Wilde",
"What you get by achieving your goals is not as important as what you become by achieving your goals. - Zig Ziglar",
"What you lack in talent can be made up with desire, hustle and giving 110% all the time. - Don Zimmer",
"Whatever the mind of man can conceive and believe, it can achieve. - Napoleon Hill",
"Whatever you can do, or dream you can, begin it. Boldness has genius, power and magic in it. - Johann Wolfgang von Goethe",
"Whatever you vivdly imagine, ardently desire, sincerely believe, and enthusiastically act upon... must inevitably come to pass! - Paul J. Meyer",
"When everything seems to be going against you, remember that the airplane takes off against the wind, not with it. - Henry Ford",
"When I let go of what I am, I become what I might be. - Lao Tzu",
"When one door of happiness closes, another opens, but often we look so long at the closed door that we do not see the one that has been opened for us. - Helen Keller",
"When we strive to become better than we are, everything around us becomes better too. - Paulo Coelho",
"When you reach the end of your rope, tie a knot in it and hang on. - Franklin D. Roosevelt",
"Whenever you see a successful business, someone once made a courageous decision. - Peter F. Drucker",
"Whenever you see a successful person you only see the public glories, never the private sacrifices to reach them. - Vaibhav Shah",
"Whether you think you can or you think you can't, you're right. - Henry Ford",
"Who sows virtue reaps honor. - Leonardo da Vinci",
"Winning isn't everything, but wanting to win is. - Vince Lombardi",
"Without hard work, nothing grows but weeds. - Gordon B. Hinckley",
"Work to become, not to acquire. - Elbert Hubbard",
"You are never too old to set another goal or to dream a new dream. - C. S. Lewis",
"You become what you believe. - Oprah Winfrey",
"You can never cross the ocean until you have the courage to lose sight of the shore. - Christopher Columbus",
"You can't build a reputation on what you are going to do. - Henry Ford",
"You can't cross the sea merely by standing and staring at the water. - Rabindranath Tagore",
"You can't use up creativity. The more you use, the more you have. - Maya Angelou",
"You have to learn the rules of the game. And then you have to play better than anyone else. - Albert Einstein",
"You may be disappointed if you fail, but you are doomed if you don't try. - Beverly Sills",
"You miss 100% of the shots you don't take. - Wayne Gretzky",
"You must be the change you wish to see in the world. - Mahatma Gandhi",
"You never know what motivates you. - Cicely Tyson",
"Your imagination is your preview of life's coming attractions. - Albert Einstein",
"Your time is limited, so don't waste it living someone else's life. - Steve Jobs",
"Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. As with all matters of the heart, you'll know when you find it. - Steve Jobs",
"All our dreams can come true, if we have the courage to pursue them. - Walt Disney",
"The secret of getting ahead is getting started. - Mark Twain",
"I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life and that is why I succeed. - Michael Jordan",
"Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve. - Mary Kay Ash",
"Only the paranoid survive. - Andy Grove",
"It’s hard to beat a person who never gives up. - Babe Ruth",
"I wake up every morning and think to myself, ‘How far can I push this company in the next 24 hours?’ - Leah Busque",
"We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes―understanding that failure is not the opposite of success, it’s part of success. - Arianna Huffington",
"Write it. Shoot it. Publish it. Crochet it. Sauté it. Whatever. MAKE. - Joss Whedon",
"If people are doubting how far you can go, go so far that you can’t hear them anymore. - Michele Ruiz",
"You’ve gotta dance like there’s nobody watching, love like you’ll never be hurt, sing like there’s nobody listening, and live like it’s heaven on earth. - William W. Purkey",
"Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten. - Neil Gaiman",
"When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us. - Helen Keller",
"Do one thing every day that scares you. - Eleanor Roosevelt",
"It’s no use going back to yesterday, because I was a different person then. - Lewis Carroll",
"Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers. - Socrates",
"Do what you feel in your heart to be right―for you’ll be criticized anyway. - Eleanor Roosevelt",
"Happiness is not something ready made. It comes from your own actions. - Dalai Lama XIV",
"Whatever you are, be a good one. - Abraham Lincoln",
"Imagination is everything. It is the preview of life's coming attractions. - Albert Einstein",
"If we have the attitude that it’s going to be a great day it usually is. - Catherine Pulsifier",
"You can either experience the pain of discipline or the pain of regret. The choice is yours. - Unknown",
"Impossible is just an opinion. - Paulo Coelho",
"Your passion is waiting for your courage to catch up. - Isabelle Lafleche",
"Magic is believing in yourself. If you can make that happen, you can make anything happen. - Johann Wolfgang Von Goethe",
"If something is important enough, even if the odds are stacked against you, you should still do it. - Elon Musk",
"Hold the vision, trust the process. - Unknown",
"People who wonder if the glass is half empty or full miss the point. The glass is refillable. - Unknown",
"It’s Monday … time to motivate and make dreams and goals happen. Let’s go! - Heather Stillufsen",
"It was a Monday and they walked on a tightrope to the sun. - Marcus Zusak",
"Goodbye, blue Monday. - Kurt Vonnegut",
"So. Monday. We meet again. We will never be friends—but maybe we can move past our mutual enmity toward a more positive partnership. - Julio-Alexi Genao",
"When life gives you Monday, dip it in glitter and sparkle all day. - Ella Woodword",
"All Motivation Mondays need are a little more coffee and a lot more mascara. - Unknown",
"I’m alive, motivated and ready to slay the day #MONSLAY. - Unknown",
"Oh! It’s Friday again. Share the love that was missing during the week. In a worthy moment of peace and bliss. - S. O’Sade",
"Friday sees more smiles than any other day of the workweek! - Kate Summers",
"Every Friday, I like to high five myself for getting through another week on little more than caffeine, willpower, and inappropriate humor. - Nanea Hoffman",
"When you leave work on Friday, leave work. Don’t let technology follow you throughout your weekend (answering text messages and emails). Take a break. You will be more refreshed to begin the workweek if you have had a break. - Catherine Pulsifer",
"Make a Friday a day to celebrate work well done that you can be proud of knowing that you just didn’t put in time to the next paycheck. - Byron Pulsifer",
"Although I understand that all days are equal with 24 hours each, most of us agree that Friday is the longest day of the week and Sunday the shortest. - D.S. Mixell",
"This Friday, finish your work and be done. Look forward to the weekend and have some fun! - Kate Summers",
"Friday. The golden child of the weekdays. The superhero of the workweek. The welcome wagon to the weekend. - Unknown",
"Happy Wednesday! Cast your love to all, trust in the team to which you are joined, and provide encouragement to fellow human beings. - Byron Pulsifer",
"Happy Wednesday! You are who you are; be happy with what you are called to do. Do not pretend to be like someone else for your gifts are unique to help lead you to the success as only you can define. Have a good day. - Byron Pulsifer",
"Happy Wednesday! Love all, trust a few, do wrong to none. - William Shakespeare",
"Happy Wednesday! Happiness is an attitude. We either make ourselves miserable, or happy and strong. The amount of work is the same. - Unknown",
"Wednesdays will always bring smiles for the second half of the week. - Anthony T. Hincks",
"To some, it’s Hump Day. To us, it’s Wednesday’s getting its ass kicked and Thursday just asking Friday to switch places. - Dwayne Johnson",
"Wednesday: Halfway to the weekend! Enjoy your day! - Unknown",
"On Wednesday they’re feelin’ fine again. - Johnny Cash",
"Happy Thursday! Greet your problems and decisions with peace and calm. Use your inner wisdom to evaluate and make smart decisions for yourself! You got this! - Tracey Edmonds",
"Some people call it Thursday, I like to call it Friday Eve. - Unknown",
"Happy Thursday! Change your life today; don’t gamble on the future, act now, without delay. - Simone de Beauvoir",
"Thursday, I forecast as mostly sunny. It’s a much-needed break. - John Farley",
"Thursday is perhaps the worst day of the week. It’s nothing in itself; it just reminds you that the week has been going on too long. - Nicci French",
"Thursday is my favorite day to plan how I’m going to get out of the plans I already made for the weekend. - Unknown",
"Make your snacks on Sunday, and plan to cook with your family for at least two nights a week. - Anya Taylor-Joy",
"Sunday clears away the rust of the whole week. - Joseph Addison",
"Sunday is the perfect day to refuel your soul and to be grateful for each and every one of your blessings. - Unknown",
"Sunday is a perfect day to choose a new path in life, don’t be afraid of changes, they come when they are really needed. Have a wonderful Sunday. - Unknown",
"Well, there’s one thing to be said for Sunday. It’s the day when we can all take a break from the hectic pace of the week and just relax. Enjoy your Sunday! - Unknown",
"Sunday is a day to clear the mind of all that has transpired the week before. - Byron Pulsifer",
"The frantic pace of the week can take its toll, but Sunday is a day to recharge the batteries and prepare for the challenges ahead. - Unknown",
"Saturday is a day to enjoy the fruits of your labor from the week, to spend time with family and friends, and to recharge for the week ahead. - Unknown",
"On Saturday, we can all take a much-needed break from the stresses of the work week and just enjoy some time for ourselves. - Unknown",
"Saturday is a day to relax and recharge, to spend time with loved ones, and to do the things that make you happy. - Unknown",
"Saturday is the perfect day to do nothing and everything all at the same time. - Unknown",
"The weekend is a time to recharge your batteries, spend time with loved ones, and do the things you love. - Unknown",
"The weekend is finally here! Time to relax and enjoy yourself. - Unknown",
"Weekends are a bit like rainbows; they look good from a distance but disappear when you get up close to them. - John Shirley",
"The weekend is the perfect time to recharge your batteries and forget about all your worries. - Unknown",
"Weekends don’t count unless you spend them doing something completely pointless. - Bill Watterson",
"It’s a new day. I’m alive. I’m blessed. God is good. God is great. Have a blessed day! - Unknown",
"A good day is a good day. A bad day is a good story. - Glennon Melton",
"Any day above ground is a good day. Before you complain about anything, be thankful for your life and the things that are still with good. - Germany Kent",
"Every day is a good day to be alive, whether the sun’s shining or not. - Marty Robbins",
"I get up every morning and it’s going to be a good day. You never know when it’s going to be over, so I refuse to have a bad day. - Paul Henderson",
"It was a good day to be alive. It usually is. - Stephen King",
"It’s a good day for a good day. - Unknown",
"Every single day is a good day no matter how bright or dark it is, because it always brings an opportunity to start a positive beginning in your life. - Edmond Mbiaka",
"Today is a good day to have a great day! - Unknown",
"Today’s a good day to have a good day. - Unknown",
"Don’t live your life regretting yesterday. Live your life so tomorrow won’t be full of regrets. - Unknown",
"You have to remember that the hard days are what make you stronger. The bad days make you realize what a good day is. If you never had any bad days, you would never have that sense of accomplishment! - Aly Raisman",
"When you’re wide awake, say it for goodness sake, it’s gonna be a great day. - Paul McCartney",
"We don’t have a great day, we make it a great day. - Frosty Westering",
"On a good day, when you have a clear plan, you are able to execute whatever you wanted. - Jasprit Bumrah",
"It’s time to start living the life you’ve imagined. - Henry James",
"Love. Fall in love and stay in love. Write only what you love, and love what you write. The key word is love. You have to get up in the morning and write something you love, something to live for. - Ray Bradbury",
"I hope everyone that is reading this is having a really good day. And if you are not, just know that in every new minute that passes you have an opportunity to change that. - Gillian Anderson",
"I just want people to take a step back, take a deep breath and actually look at something with a different perspective. But most people will never do that. - Brian McKnight",
"Even if you're on the right track, you'll get run over if you just sit there. - Will Rogers",
"Life is like riding a bicycle. To keep your balance, you must keep moving. - Albert Einstein",
"Nothing is impossible, the word itself says, 'I'm possible!' - Audrey Hepburn",
"The only thing worse than starting something and failing … is not starting something. - Seth Godin",
"Life changes very quickly, in a very positive way, if you let it. - Lindsey Vonn",
"If you don't like the road you're walking, start paving another one. - Dolly Parton",
"All great ideas start as weird ideas. - Unknown",
"You can’t have a better tomorrow if you are thinking about yesterday all the time. - Charles Kettering",
"What you do makes a difference, and you have to decide what kind of difference you want to make. - Jane Goodall",
"Being a successful person is not necessarily defined by what you have achieved, but by what you have overcome. - Fannie Flagg",
"Failure is the condiment that gives success its flavor. - Truman Capote",
"If you know you are on the right track, if you have this inner knowledge, then nobody can turn you off… no matter what they say. - Barbara McClintock",
"I learned a long time ago that there is something worse than missing the goal, and that’s not pulling the trigger. - Mia Hamm",
"You cannot be lonely if you like the person you're alone with. - Wayne Dyer",
"No one is to blame for your future situation but yourself. If you want to be successful, then become 'Successful.' - Jaymin Shah",
"Opportunity is missed by most people because it is dressed in overalls and looks like work. - Thomas Edison",
"Yesterday’s home runs don't win today's games. - Babe Ruth",
"The only real mistake is the one from which we learn nothing. - Henry Ford",
"The successful man will profit from his mistakes and try again in a different way. - Dale Carnegie",
"Success is a lousy teacher. It seduces smart people into thinking they can’t lose. - Bill Gates",
"Failure is success in progress. - Albert Einstein",
"The difference between successful people and others is how long they spend feeling sorry for themselves. - Barbara Corcoran",
"The only thing that overcomes hard luck is hard work. - Harry Golden",
"Your positive action combined with positive thinking results in success. - Shiv Khera",
"Success is getting what you want, happiness is wanting what you get. - W. P. Kinsella",
"Success is dependent on effort. - Sophocles",
"The successful warrior is the average man, with laser-like focus. - Bruce Lee",
"If you really look closely, most overnight successes took a long time. - Steve Jobs",
"Self-belief and hard work will always earn you success. - Virat Kohli",
"Success is how high you bounce when you hit bottom. - George S. Patton",
"Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
"Success seems to be connected with action. Successful people keep moving. They make mistakes but they don't quit. - Conrad Hilton",
"Success is not in what you have, but who you are. - Bo Bennett",
"The difference between who you are and who you want to be is what you do. - Unknown",
"Success is liking yourself, liking what you do, and liking how you do it. - Maya Angelou",
"Success is stumbling from failure to failure with no loss of enthusiasm. - Winston S. Churchill",
"Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. - Albert Schweitzer",
"Success is a state of mind. If you want success, start thinking of yourself as a success. - Joyce Brothers",
"Success comes from knowing that you did your best to become the best that you are capable of becoming. - John Wooden",
"The secret of success is to do the common thing uncommonly well. - John D. Rockefeller Jr.",
"Success is the sum of small efforts - repeated day in and day out. - Robert Collier",
"Success is not final; failure is not fatal: It is the courage to continue that counts. - Winston S. Churchill",
"The road to success and the road to failure are almost exactly the same. - Colin R. Davis",
"Don’t be distracted by criticism. Remember — the only taste of success some people get is to take a bite out of you. - Zig Ziglar",
"Success is only meaningful and enjoyable if it feels like your own. - Michelle Obama",
"I never dreamed about success. I worked for it. - Estée Lauder",
"The only thing standing between you and outrageous success is continuous progress. - Dan Waldschmidt",
"Success is the result of perfection, hard work, learning from failure, loyalty, and persistence. - Colin Powell",
"Coming together is a beginning; keeping together is progress; working together is success. - Edward Everett Hale",
"Ambition is the path to success. Persistence is the vehicle you arrive in. - Bill Bradley",
"If you really want to do something, you'll find a way. If you don't, you'll find an excuse. - Jim Rohn",
"A successful man is one who can lay a firm foundation with the bricks others have thrown at him. - David Brinkley",
"The successful man will profit from his mistakes and try again in a different way. - Dale Carnegie",
"Success is peace of mind which is a direct result of self-satisfaction in knowing you did your best to become the best you are capable of becoming. - John Wooden",
"Success is best when it's shared. - Howard Schultz",
"Success is a journey not a destination. - Ben Sweetland",
"Success? I don't know what that word means. I'm happy. But success, that goes back to what in somebody's eyes success means. For me, success is inner peace. That's a good day for me. - Denzel Washington",
"Success is often achieved by those who don't know that failure is inevitable. - Coco Chanel",
"Choose a job you love, and you will never have to work a day in your life. - Confucius",
"Success in business requires training and discipline and hard work. But if you’re not frightened by these things, the opportunities are just as great today as they ever were. - David Rockefeller",
"To be successful, you have to have your heart in your business, and your business in your heart. - Thomas Watson Sr.",
"Success is about creating value. - Candice Carpenter",
"The secret of success in every field is redefining what success means to you. It can't be your parent's definition, the media's definition, or your neighbor's definition. Otherwise, success will never satisfy you. - RuPaul",
"Strive not to be a success, but rather to be of value. - Albert Einstein",
"Success isn't about how much money you make. It's about the difference you make in people's lives. - Michelle Obama",
"Success is going from failure to failure without losing enthusiasm. - Winston Churchill",
"The secret of success is constancy to purpose. - Benjamin Disraeli",
"The only place where success comes before work is in the dictionary. - Vidal Sassoon",
"Success is 99 percent failure. - Soichiro Honda",
"If you have no critics you'll likely have no success. - Malcolm X",
"Living our life deeply and with happiness, having time to care for our loved ones, this is another kind of success, another kind of power, and it is much more important. - Thich Nhat Hanh",
"Success isn't always about greatness. It's about consistency. Consistent hard work leads to success. Greatness will come. - Dwayne Johnson",
"The biggest challenge after success is shutting up about it. - Criss Jami",
"Applause waits on success. - Benjamin Franklin",
"Nothing succeeds like success. - Alexandre Dumas",
"We must walk consciously only part way toward our goal, and then leap in the dark to our success. - Henry David Thoreau",
"The difference between successful people and very successful people is that very successful people say 'no' to almost everything. - Warren Buffett",
"One important key to success is self-confidence. An important key to self-confidence is preparation. - Arthur Ashe",
"Success comes in cans; failure in can'ts. - Wilfred Peterson",
"However difficult life may seem, there is always something you can do and succeed at. - Stephen Hawking",
"He has achieved success who has lived well, laughed often and loved much. - Bessie Anderson Stanley",
"Measure your success according to fun and creativity. - Anita Roddick",
"Sitting quietly, doing nothing, Spring comes and the grass grows, by itself. - Basho",
"If you want to live a happy life, tie it to a goal, not to people or things. - Albert Einstein",
"The whole secret of a successful life is to find out what is one's destiny to do, and then do it. - Henry Ford",
"If you want to be happy, set a goal that commands your thoughts, liberates your energy, and inspires your hopes. - Andrew Carnegie",
"Happiness cannot be traveled to, owned, earned, worn, or consumed. Happiness is the spiritual experience of living every minute with love, grace, and gratitude. - Denis Waitley",
"It is only when we take chances, when our lives improve. The initial and the most difficult risk that we need to take is to become honest. - Walter Anderson",
"Only put off until tomorrow what you are willing to die having left undone. - Pablo Picasso",
"We become what we think about most of the time, and that's the strangest secret. - Earl Nightingale",
"The only place where success comes before work is in the dictionary. - Vidal Sassoon",
"Though no one can go back and make a brand-new start, anyone can start from now and make a brand-new ending. - Carl Bard",
"Don't let yesterday take up too much of today's. - Will Rogers",
"The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty. - Winston Churchill",
"If you are working on something that you really care about, you don’t have to be pushed. The vision pulls you. - Steve Jobs",
"If you can't explain it simply, you don't understand it well enough. - Albert Einstein",
"People often say that motivation doesn't last. Well, neither does bathing--that's why we recommend it daily. - Zig Ziglar",
"Working hard for something we don't care about is called stressed; working hard for something we love is called passion. - Simon Sinek",
"I’d rather regret the things I’ve done than regret the things I haven’t done. - Lucille Ball",
"I didn't get there by wishing for it or hoping for it, but by working for it. - Estée Lauder",
"Always do your best. What you plant now, you will harvest later. - Og Mandino",
"The key to life is accepting challenges. Once someone stops doing this, he's dead. - Bette Davis",
"Move out of your comfort zone. You can only grow if you are willing to feel awkward and uncomfortable when you try something new. - Brian Tracy",
"Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine",
"Don't let the fear of losing be greater than the excitement of winning. - Robert Kiyosaki",
"How dare you settle for less when the world has made it so easy for you to be remarkable? - Seth Godin",
"Energy and persistence conquer all things. - Benjamin Franklin",
"Perseverance is failing 19 times and succeeding the 20th. - Julie Andrews",
"Grit is that ‘extra something' that separates the most successful people from the rest. It's the passion, perseverance, and stamina that we must channel in order to stick with our dreams until they become a reality. - Travis Bradberry",
"Failure after long perseverance is much grander than never to have a striving good enough to be called a failure. - George Eliot",
"The secret of success is to do the common thing uncommonly well. - John D. Rockefeller Jr.",
"I find that the harder I work, the more luck I seem to have. - Thomas Jefferson",
"If you are not willing to risk the usual, you will have to settle for the ordinary. - Jim Rohn",
"All progress takes place outside the comfort zone. - Michael John Bobak",
"Don't wish it were easier, wish you were better. - Jim Rohn",
"It is your determination and persistence that will make you a successful person. - Kenneth J Hutchins",
"You can waste your lives drawing lines. Or you can live your life crossing them. - Shonda Rhimes",
"If you really want to do it, you do it. There are no excuses. - Bruce Nauman",
"Determine that the thing can and shall be done, and then we shall find the way. - Abraham Lincoln",
"Be sure you put your feet in the right place, then stand firm. - Abraham Lincoln",
"I don't want to get to the end of my life and find that I lived just the length of it. I want to have lived the width of it as well. - Diane Ackerman",
"Motivation is what gets you started. Habit is what keeps you going. - Jim Rohn",
"You must expect great things of yourself before you can do them. - Michael Jordan",
"You don't have to see the whole staircase, just take the first step. - Martin Luther King Jr.",
"Don't stop when you're tired. Stop when you're done. - Unknown",
"You may have to fight a battle more than once to win it. - Margaret Thatcher",
"Dream as if you'll live forever, live as if you'll die today. - James Dean",
"The difference between the impossible and the possible lies in a person's determination. - Tommy Lasorda",
"To be a champion, I think you have to see the big picture. - Summer Sanders",
"Obsessed is the word the lazy use to describe dedicated. - Russell Warren",
"If we didn't do what we loved, we wouldn't exist. - Adonis",
"If it doesn't challenge you, it won't change you. - Unknown",
"The greater the difficulty, the more the glory in surmounting it. - Epicurus",
"We can do anything we want to if we stick to it long enough. - Helen Keller",
"It isn't the mountains ahead to climb that wear you out; it's the pebble in your shoe. - Muhammad Ali",
"If your actions inspire others to dream more, learn more, do more and become more, you are a leader. - John Quincy Adams",
"Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
"Our greatest glory is not in never falling, but in rising every time we fall. - Confucius",
"All you need is the plan, the road map, and the courage to press on to your destination. - Earl Nightingale",
"Though no one can go back and make a brand new start, anyone can start from now and make a brand new ending. - Carl Bard",
"Don't be pushed by your problems; be led by your dreams. - Unknown",
"Don't mistake activity with achievement. - John Wooden",
"One day or day one. You decide. - Unknown",
"What we fear doing most is usually what we most need to do. - Tim Ferriss",
"Impossible is for the unwilling. - John Keats",
"No pressure, no diamonds. - Thomas Carlyle",
"Believe you can and you're halfway there. - Theodore Roosevelt",
"Stay close to anything that makes you glad you are alive. - Hafez",
"You do not find the happy life. You make it. - Camilla Eyring Kimball",
"You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. - Dr. Seuss",
"If there is no wind, row. - Latin Proverb",
"Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
"Make each day your masterpiece. - John Wooden",
"Your time is limited, so don’t waste it living someone else’s life. - Steve Jobs",
"The best revenge is massive success. - Frank Sinatra",
"Don't wait. The time will never be just right. - Napoleon Hill",
"Happiness is not by chance, but by choice. - Jim Rohn",
"Life changes very quickly, in a very positive way, if you let it. - Lindsey Vonn",
"Keep calm and carry on. - Winston Churchill",
"There is nothing impossible to they who will try. - Alexander the Great",
"Keep your face to the sunshine and you can not see a shadow. - Unknown",
"In a gentle way, you can shake the world. - Mahatma Gandhi",
"Let your soul stand cool and composed before a million universe. - Walt Whitman",
"The real difficulty is to overcome how you think about yourself. - Maya Angelou",
"Turn your wounds into wisdom. - Oprah Winfrey",
"Wherever you go, go with all your heart. - Confucius",
"We can do anything we want to if we stick to it long enough. - Helen Keller",
"Begin anywhere. - John Cage",
"I choose to make the rest of my life the best of my life. - Louise Hay",
"Nothing can dim the light that shines from within. - Maya Angelou",
"Be so good they can’t ignore you. - Steve Martin",
"Take the risk or lose the chance. - Unknown",
"Yesterday you said tomorrow. Just do it. - Nike",
"The elevator to success is out of order. You’ll have to use the stairs, one step at a time. - Joe Girard",
"Some people want it to happen, some wish it would happen, others make it happen. - Michael Jordan",
"Don’t be afraid to give up the good to go for the great. - John D. Rockefeller",
"Don’t quit. Suffer now and live the rest of your life as a champion. - Muhammad Ali",
"A hill is just another opportunity to show that your determination and perseverance can level anything in your path to success. - Michelle C. Ustaszeski",
"Don’t tell everyone your plans, instead show them your results. - Unknown",
"We can do no great things, only small things with great love. - Mother Teresa",
"I learned this, at least, by my experiment; that if one advances confidently in the direction of his dreams, and endeavors to live the life which he has imagined, he will meet with a success unexpected in common hours. - Henry David Thoreau",
"Make it happen. Shock everyone. - Unknown",
"Work hard and be kind and amazing things will happen. - Conan O’Brien",
"Never stop doing your best just because someone doesn’t give you credit. - Kamari aka Lyrikal",
"Work hard in silence, let your success be the noise. - Frank Ocean",
"Work hard now. Suffer and sacrifice now. So that you can live the rest of your life as a champion. - Apolo Ohno",
"Never stop learning, because life never stops teaching. - Unknown",
"Winners are not people never fail, but people who never quit. - Unknown",
"It takes nothing to join the crowd. It takes everything to stand alone. - Hans F. Hansen",
"Your talent determines what you can do. Your motivation determines how much you’re willing to do. Your attitude determines how well you do it. - Lou Holtz",
"The happiness of your life depends on the quality of your thoughts. - Marcus Aurelius",
"Intelligence is the ability to adapt to change. - Stephen Hawking",
"Leaders can let you fail and yet not let you be a failure. - Stanley McChrystal",
"Would you like me to give you a formula for success? It’s quite simple, really: Double your rate of failure. You are thinking of failure as the enemy of success. But it isn’t at all. You can be discouraged by failure or you can learn from it, so go ahead and make mistakes. Make all you can. Because remember, that’s where you will find success. - Thomas J. Watson",
"Be happy with what you have while working for what you want. - Helen Keller",
"Sunshine all the time makes a desert. - Arabic proverb",
"The big lesson in life is never be scared of anyone or anything. - Frank Sinatra",
"I always wanted to be somebody, but now I realise I should have been more specific. - Lily Tomlin",
"If you think you are too small to make a difference, try sleeping with a mosquito. - Dalai Lama",
"Don't worry about failure. You only have to be right once. - Drew Houston",
"You carry the passport to your own happiness. - Diane Von Furstenberg",
"Never let success get to your head and never let failure get to your heart. - Drake",
"The greatest discovery of my generation is that a human being can alter his life by altering his attitudes. - William James",
"Anyone who has ever made anything of importance was disciplined. - Andrew Hendrixson",
"Don’t spend time beating on a wall, hoping to transform it into a door. - Coco Chanel",
"Optimism is the one quality more associated with success and happiness than any other. - Brian Tracy",
"Always keep your eyes open. Keep watching. Because whatever you see can inspire you. - Grace Coddington",
"What you get by achieving your goals is not as important as what you become by achieving your goals. - Henry David Thoreau",
"If the plan doesn’t work, change the plan, but never the goal. - Unknown",
"Don’t focus on negative things; focus on the positive, and you will flourish. - Alek Wek",
"I surround myself with good people who make me feel great and give me positive energy. - Ali Krieger",
"The only thing standing in the way between you and your goal is the BS story you keep telling yourself as to why you can’t achieve it. - Jordan Belfort",
"The only thing worse than starting something and failing… is not starting something. - Seth Godin",
"Don’t think, just do. - Horace",
"Everything is learnable. - Brian Tracy",
"Don’t worry about failure; you only have to be right once. - Drew Houston",
"Life is like a movie, write your own ending. Keep believing, keep pretending. - Jim Henson",
"Don’t talk, just act. Don’t say, just show. Don’t promise, just prove. - Unknown",
"It does not matter how slowly you go so long as you do not stop. - Confucius",
"Never confuse a single defeat with a final defeat. - F. Scott Fitzgerald",
"Perseverance is not a long race; it is many short races one after another. - Walter Elliot",
"Someone, at some point, came up with this very bad idea that an ordinary individual couldn't make a difference in the world. I think that's just a horrible thing. - John Skoll",
"Work like there is someone working twenty-four hours a day to take it away from you. - Mark Cuban",
"I am thankful for a problem grudge, for it can in no way be pleasing to me. - Unknown",
"Be a positive energy tranceiver. Give everything you have to be your best, and good things will come. - Unknown",
"You cannot plow a field by turning it over in your mind. To begin, begin. - Gordon B. Hinckley",
"Give your dreams all you’ve got and you’ll be amazed at the energy that comes out of you. - William James",
"Strength shows not only in the ability to persist, but in the ability to start over. - F. Scott Fitzgerald",
"As long as you hate, there will be people to hate. - George Harrison",
"Make sure your worst enemy doesn’t live between your own two ears. - Laird Hamilton",
"It is a man’s own mind, not his enemy or foe, that lures him to evil ways. - Buddha",
"The greatest weapon against stress is the ability to choose one thought over another. - William James",
"Pessimism never won any battle. - Dwight D. Eisenhower",
"If you hear a voice within you say 'you cannot paint,' then by all means paint, and that voice will be silenced. - Vincent van Gogh",
"People begin to become successful the minute they decide to be. - Harvey MacKay",
"Hold the vision, trust the process. - Unknown",
"May your choices reflect your hopes, not your fears. - Nelson Mandela",
"Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart. - Roy T. Bennett",
"Instead of worrying about what you cannot control, shift your energy to what you can create. - Roy T. Bennett",
"Take responsibility of your own happiness, never put it in other people’s hands. - Roy T. Bennett",
"Be mindful. Be grateful. Be positive. Be true. Be kind. - Roy T. Bennett",
"Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy. - Roy T. Bennett",
"Life becomes easier and more beautiful when we can see the good in other people. - Roy T. Bennett",
"Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
"Follow your heart, listen to your inner voice, stop caring about what others think. - Roy T. Bennett",
"Start each day with a positive thought and a grateful heart. - Roy T. Bennett",
"Be brave to stand for what you believe in even if you stand alone. - Roy T. Bennett",
"Do what is right, not what is easy nor what is popular. - Roy T. Bennett",
"If you have a strong purpose in life, you don’t have to be pushed. Your passion will drive you there. - Roy T. Bennett",
"Always have a willing hand to help someone, you might be the only one that does. - Roy T. Bennett",
"Strong people have a strong sense of self-worth and self-awareness; they don’t need the approval of others. - Roy T. Bennett",
"Knowledge is being aware of what you can do. Wisdom is knowing when not to do it. - Anonymous",
"Always remember people who have helped you along the way, and don’t forget to lift someone up. - Roy T. Bennett",
"It’s only after you’ve stepped outside your comfort zone that you begin to change, grow, and transform. - Roy T. Bennett",
"More smiling, less worrying. More compassion, less judgment. More blessed, less stressed. More love, less hate. - Roy T. Bennett",
"Take responsibility of your own happiness, never put it in other people’s hands. - Roy T. Bennett",
"Be the reason someone smiles. Be the reason someone feels loved and believes in the goodness in people. - Roy T. Bennett",
"Accept yourself, love yourself, and keep moving forward. If you want to fly, you have to give up what weighs you down. - Roy T. Bennett",
"Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine. - Roy T. Bennett",
"Live the Life of Your Dreams: Be brave enough to live the life of your dreams according to your vision and purpose instead of the expectations and opinions of others. - Roy T. Bennett",
"The past is a place of reference, not a place of residence; the past is a place of learning, not a place of living. - Roy T. Bennett",
"Make improvements, not excuses. Seek respect, not attention. - Roy T. Bennett",
"Life is about accepting the challenges along the way, choosing to keep moving forward, and savoring the journey. - Roy T. Bennett",
"Time doesn’t heal emotional pain, you need to learn how to let go. - Roy T. Bennett",
"Nothing can disturb your peace of mind unless you allow it to. - Roy T. Bennett",
"You will never follow your own inner voice until you clear up the doubts in your mind. - Roy T. Bennett",
"Being grateful does not mean that everything is necessarily good. It just means that you can accept it as a gift. - Roy T. Bennett",
"Always find opportunities to make someone smile, and to offer random acts of kindness in everyday life. - Roy T. Bennett",
"Courage is feeling fear, not getting rid of fear, and taking action in the face of fear. - Roy T. Bennett",
"Failure is a bend in the road, not the end of the road. Learn from failure and keep moving forward. - Roy T. Bennett",
"To learn something new, you need to try new things and not be afraid to be wrong. - Roy T. Bennett",
"Sometimes all a person wants is an empathetic ear; all he or she needs is to talk it out. Just offering a listening ear and an understanding heart for his or her suffering can be a big comfort. - Roy T. Bennett",
"It’s your life; you don’t need someone’s permission to live the life you want. Be brave to live from your heart. - Roy T. Bennett",
"Be brave enough to live the life of your dreams according to your vision and purpose instead of the expectations and opinions of others. - Roy T. Bennett",
"To have what you have never had, you have to do what you have never done. - Roy T. Bennett",
"Never lose hope. Storms make people stronger and never last forever. - Roy T. Bennett",
"The biggest wall you have to climb is the one you build in your mind: Never let your mind talk you out of your dreams, trick you into giving up. Never let your mind become the greatest obstacle to success. To get your mind on the right track, the rest will follow. - Roy T. Bennett",
"Consistency is the true foundation of trust. Either keep your promises or do not make them. - Roy T. Bennett",
"Stop doing what is easy. Start doing what is right. - Roy T. Bennett",
"Maturity is when you stop complaining and making excuses, and start making changes. - Roy T. Bennett",
"Do not fear failure but rather fear not trying. - Roy T. Bennett",
"Stop doing what is easy or popular. Start doing what is right. - Roy T. Bennett",
"Changing your outside world cannot make you happy if you are an unhappy person. The real personal change can only happen from the inside out. If you firstly create the change within yourself, you can turn your life around. - Roy T. Bennett",
"Unless you try to do something beyond what you have already mastered, you will never grow. - Roy T. Bennett",
"The one who falls and gets up is stronger than the one who never tried. Do not fear failure but rather fear not trying. - Roy T. Bennett",
"Gratitude builds a bridge to abundance. - Roy T. Bennett",
"Once you realize you deserve a bright future, letting go of your dark past is the best choice you will ever make. - Roy T. Bennett",
"Always believe in yourself and always stretch yourself beyond your limits. Your life is worth a lot more than you think because you are capable of accomplishing more than you know. You have more potential than you think, but you will never know your full potential unless you keep challenging yourself and pushing beyond your own self imposed limits. - Roy T. Bennett",
"Comfort zone: Simply means the routine of one’s daily life – it is a psychological state in which one feels familiar, safe, at ease, and secure. - Roy T. Bennett",
"Believe in your infinite potential. Your only limitations are those you set upon yourself. - Roy T. Bennett",
"Most of us must learn to love people and use things rather than loving things and using people. - Roy T. Bennett",
"Surround yourself with people who believe in your dreams",
    ]
    await update.message.reply_text(f"💡 *“{random.choice(quotes)}”*", parse_mode='Markdown')


async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    team_text = (
        "**👥 The OpenStart Team**\n\n"
        "Our team is a global collaboration of passionate young leaders:\n"
        "▪️ **Vikusyaaa** (Ukraine)\n"
        "▪️ **Rakesh Kumar** (India)\n"
        "▪️ **Cheedhe** (Tunisia)"
    )
    await update.message.reply_text(team_text, parse_mode='Markdown')


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Upcoming events and deadlines will be announced here soon. Stay tuned!")


async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 We are compiling a library of guides, books, and tools for young founders. This feature will be available shortly!")


async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    community_text = "🌐 Join our global community of young innovators on Discord to connect, collaborate, and share ideas!"
    keyboard = [[InlineKeyboardButton("Join Discord", url="https://discord.gg/your-invite-link")]]  # Replace with real link
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(community_text, reply_markup=reply_markup)


async def mentor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mentor_text = "🎓 We will initially assign a mentor for you related to your startup niche and business tech."
    await update.message.reply_text(mentor_text)


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faq_text = (
        "**❔ Frequently Asked Questions**\n\n"
        "**Q: Who can apply for OpenStart?**\n"
        "A: Ambitious high school students from anywhere in the world!\n\n"
        "**Q: Is there a fee to participate?**\n"
        "A: Our goal is to make our programs as accessible as possible. Details about costs will be available soon."
    )
    await update.message.reply_text(faq_text, parse_mode='Markdown')


async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apply_text = (
        "📝 As of now, you can either visit our website or fill out this Google Form. "
        "We will respond to you within 48 hours."
    )
    keyboard = [[InlineKeyboardButton("Fill Application Form", url="https://forms.gle/oqeBL4fRJXTnTymh9")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(apply_text, reply_markup=reply_markup)


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = "📩 You can visit our website to get in touch with the OpenStart team."
    await update.message.reply_text(contact_text)


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = "💬 You can share your feedback with us by filling out this form."
    keyboard = [[InlineKeyboardButton("Share Feedback", url="https://forms.gle/5azM3K8h7ek2B2cn8")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(feedback_text, reply_markup=reply_markup)

# --- Message Handling ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(greeting in text for greeting in ["hello", "hi", "hey"]):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}! Use /help to see what I can do.")
        raise ApplicationHandlerStop

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that. Try /help for a list of commands.")

# --- Bot Setup ---

async def post_init(application: Application):
    bot_commands = [(command, description) for command, description in COMMANDS.items()]
    await application.bot.set_my_commands(bot_commands)
    print("Bot commands set successfully!")

def main():
    if not TOKEN:
        logging.error("TELEGRAM_TOKEN is not set!")
        return
    if not NEWS_API_KEY:
        logging.error("NEWS_API_KEY is not set!")
        return

    # Start Flask server in background
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Start Telegram bot
    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("quote", quote))
    application.add_handler(CommandHandler("team", team))
    application.add_handler(CommandHandler("events", events))
    application.add_handler(CommandHandler("resources", resources))
    application.add_handler(CommandHandler("community", community))
    application.add_handler(CommandHandler("mentor", mentor))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("apply", apply))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("feedback", feedback))

    # Fallbacks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("Starting Telegram bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()

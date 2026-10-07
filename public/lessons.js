/* English Step-Up — lesson content (shared by the student and teacher pages). */

window.LESSONS = [

{
  id: 1,
  icon: "👋",
  title: "English Familiarization",
  subtitle: "Get comfortable with common English words and simple sentences.",
  goal: "Recognize familiar English words and understand very simple sentences.",

  explanation: `
    English is made up of words that help us talk about people,
    places, animals, things, actions, feelings, and ideas.

    You already see and hear many English words every day.

    In this lesson, you do not need to memorize difficult rules.
    Your goal is simply to become comfortable recognizing common
    English words and understanding what simple sentences mean.
  `,

  explainAgain: `
    Think of English as a way of giving names and meaning to things
    around you.

    For example:

    "book" is something you can read.

    "school" is a place where students learn.

    "run" tells us an action.

    When words are placed together, they can make a sentence.

    Example:

    "The boy runs."

    This simply tells us that a boy is doing the action of running.
  `,

  examples: [
    "<strong>apple</strong> — a fruit",
    "<strong>school</strong> — a place where students learn",
    "<strong>teacher</strong> — a person who teaches",
    "<strong>run</strong> — an action",
    "<strong>The dog is sleeping.</strong> — The sentence tells us what the dog is doing."
  ],

  questions: [
    {
      question: "Which word names an animal?",
      options: ["table", "dog", "school", "jump"],
      answer: 1,
      explanation: "A dog is an animal. The other words name a thing, a place, or an action."
    },
    {
      question: "Which word names a place?",
      options: ["school", "eat", "cat", "pencil"],
      answer: 0,
      explanation: "A school is a place where students learn."
    },
    {
      question: 'What does the sentence "The girl reads a book." tell us?',
      options: ["The girl is sleeping.", "The girl is reading.", "The girl is running.", "The girl is eating."],
      answer: 1,
      explanation: 'The word "reads" tells us that the girl is reading.'
    },
    {
      question: "Which word shows an action?",
      options: ["house", "happy", "jump", "teacher"],
      answer: 2,
      explanation: '"Jump" is something a person or animal can do, so it shows an action.'
    },
    {
      question: 'What is happening in the sentence "The cat is sleeping."?',
      options: ["The cat is eating.", "The cat is sleeping.", "The cat is running.", "The cat is playing."],
      answer: 1,
      explanation: "The sentence directly tells us that the cat is sleeping."
    }
  ]
},

{
  id: 2,
  icon: "🏷️",
  title: "Naming Words",
  subtitle: "Learn words that name people, places, animals, and things.",
  goal: "Identify naming words in simple sentences.",

  explanation: `
    A naming word tells us the name of a person, place, animal, or thing.

    In grammar, a naming word is called a noun.

    Examples:

    teacher — person

    park — place

    dog — animal

    pencil — thing

    Naming words help us know who or what we are talking about.
  `,

  explainAgain: `
    A noun is simply a name.

    If a word names someone or something, it can be a noun.

    Ask yourself:

    "Is this the name of a person, place, animal, or thing?"

    If the answer is yes, it is probably a noun.
  `,

  examples: [
    "<strong>Maria</strong> is a student. — Maria names a person.",
    "We went to the <strong>market</strong>. — Market names a place.",
    "The <strong>dog</strong> barked. — Dog names an animal.",
    "I lost my <strong>pencil</strong>. — Pencil names a thing.",
    "The <strong>teacher</strong> opened the <strong>book</strong>. — Teacher and book are naming words."
  ],

  questions: [
    {
      question: 'Which word is a naming word in "The boy runs fast"?',
      options: ["the", "boy", "runs", "fast"],
      answer: 1,
      explanation: '"Boy" names a person, so it is a noun.'
    },
    {
      question: "Which word names a place?",
      options: ["hospital", "walk", "kind", "quickly"],
      answer: 0,
      explanation: "A hospital is a place."
    },
    {
      question: "Which word names a thing?",
      options: ["chair", "laugh", "happy", "slow"],
      answer: 0,
      explanation: "A chair is an object or thing."
    },
    {
      question: 'Which naming word appears in "The cat drinks water"?',
      options: ["cat", "drinks", "the", "quickly"],
      answer: 0,
      explanation: '"Cat" names an animal.'
    },
    {
      question: "Which group contains only naming words?",
      options: ["run, jump, eat", "happy, sad, tall", "teacher, school, book", "slowly, loudly, softly"],
      answer: 2,
      explanation: "Teacher, school, and book all name people, places, or things."
    }
  ]
},

{
  id: 3,
  icon: "🏃",
  title: "Action Words",
  subtitle: "Learn words that tell us what someone or something does.",
  goal: "Recognize action words in simple sentences.",

  explanation: `
    An action word tells us what a person, animal, or thing does.

    In grammar, many action words are called verbs.

    Examples:

    run

    eat

    write

    sleep

    jump

    To find the action word, ask:

    "What is the person or thing doing?"
  `,

  explainAgain: `
    Imagine watching someone.

    If you can answer:

    "What are they doing?"

    the answer is usually an action word.

    The girl runs.

    What is the girl doing?

    She runs.

    So "runs" is the action word.
  `,

  examples: [
    "The boy <strong>runs</strong>.",
    "Maria <strong>reads</strong> a book.",
    "The dog <strong>jumps</strong>.",
    "My father <strong>cooks</strong> dinner.",
    "The baby <strong>sleeps</strong>."
  ],

  questions: [
    {
      question: 'What is the action word in "The girl sings"?',
      options: ["girl", "the", "sings", "none"],
      answer: 2,
      explanation: '"Sings" tells us what the girl is doing.'
    },
    {
      question: "Which word shows an action?",
      options: ["blue", "school", "write", "teacher"],
      answer: 2,
      explanation: '"Write" is something a person can do.'
    },
    {
      question: 'What is the action word in "The dog runs outside"?',
      options: ["dog", "runs", "outside", "the"],
      answer: 1,
      explanation: '"Runs" tells us the action performed by the dog.'
    },
    {
      question: "Which group contains only action words?",
      options: ["eat, jump, read", "book, chair, school", "happy, big, red", "boy, mother, teacher"],
      answer: 0,
      explanation: "Eat, jump, and read are all actions."
    },
    {
      question: 'In "Anna opens the door," what is Anna doing?',
      options: ["door", "Anna", "opening", "standing"],
      answer: 2,
      explanation: 'The verb "opens" tells us that Anna is opening the door.'
    }
  ]
},

{
  id: 4,
  icon: "🎨",
  title: "Describing Words",
  subtitle: "Learn words that give more information about people and things.",
  goal: "Identify simple describing words.",

  explanation: `
    A describing word gives us more information about a person,
    animal, place, or thing.

    In grammar, many describing words are called adjectives.

    Examples:

    big dog

    red apple

    happy girl

    cold water

    The describing word helps us imagine something more clearly.
  `,

  explainAgain: `
    A describing word answers questions such as:

    What kind?

    What color?

    What size?

    How does it feel?

    Example:

    "a red ball"

    Ball is the thing.

    Red tells us more about the ball.

    So "red" is a describing word.
  `,

  examples: [
    "a <strong>big</strong> house",
    "a <strong>happy</strong> child",
    "a <strong>red</strong> apple",
    "a <strong>cold</strong> drink",
    "a <strong>beautiful</strong> garden"
  ],

  questions: [
    {
      question: 'What is the describing word in "The big dog barked"?',
      options: ["dog", "barked", "big", "the"],
      answer: 2,
      explanation: '"Big" tells us more about the dog.'
    },
    {
      question: "Which word is a describing word?",
      options: ["happy", "run", "school", "teacher"],
      answer: 0,
      explanation: '"Happy" describes how someone feels.'
    },
    {
      question: 'Which word describes the apple in "She ate a red apple"?',
      options: ["ate", "she", "apple", "red"],
      answer: 3,
      explanation: '"Red" tells us the color of the apple.'
    },
    {
      question: "Which phrase contains a describing word?",
      options: ["runs quickly", "blue bag", "go home", "eat lunch"],
      answer: 1,
      explanation: '"Blue" describes the bag.'
    },
    {
      question: 'In "The water is cold," which word describes the water?',
      options: ["water", "the", "cold", "is"],
      answer: 2,
      explanation: '"Cold" tells us what the water feels like.'
    }
  ]
},

{
  id: 5,
  icon: "🧱",
  title: "Building a Simple Sentence",
  subtitle: "Learn how simple English sentences are formed.",
  goal: "Recognize and build a basic complete sentence.",

  explanation: `
    A simple sentence usually tells us:

    WHO or WHAT we are talking about

    and

    WHAT happens or what they do.

    Example:

    "The boy runs."

    The boy tells us who.

    Runs tells us what he does.

    Together, they make a complete idea.
  `,

  explainAgain: `
    Think of a sentence as a complete message.

    "The girl"

    is not complete because we do not know what happened.

    "The girl reads."

    is complete.

    We know who: the girl.

    We know what she does: reads.
  `,

  examples: [
    "<strong>The dog sleeps.</strong>",
    "<strong>Maria reads.</strong>",
    "<strong>The baby cries.</strong>",
    "<strong>My father cooks dinner.</strong>",
    "<strong>The students study English.</strong>"
  ],

  questions: [
    {
      question: "Which is a complete simple sentence?",
      options: ["The girl", "Runs fast", "The girl runs.", "Because she"],
      answer: 2,
      explanation: '"The girl runs." gives us a complete idea.'
    },
    {
      question: 'In "The dog sleeps," who or what are we talking about?',
      options: ["sleeps", "dog", "the", "none"],
      answer: 1,
      explanation: 'The sentence is talking about "the dog."'
    },
    {
      question: 'In "Maria reads," what does Maria do?',
      options: ["Maria", "reads", "girl", "book"],
      answer: 1,
      explanation: 'The word "reads" tells us what Maria does.'
    },
    {
      question: "Which sentence gives a complete idea?",
      options: ["The red", "My brother plays basketball.", "In the house", "Very happy"],
      answer: 1,
      explanation: '"My brother plays basketball." tells us who and what happens.'
    },
    {
      question: "Which sentence is written correctly?",
      options: ["the boy eats.", "The boy eats.", "The boy eats", "boy eats."],
      answer: 1,
      explanation: "A sentence normally begins with a capital letter and ends with punctuation."
    }
  ]
},

{
  id: 6,
  icon: "🙋",
  title: "Who and What",
  subtitle: "Learn to identify who or what a sentence is about.",
  goal: "Answer basic WHO and WHAT questions.",

  explanation: `
    WHO questions usually ask about a person.

    WHAT questions usually ask about a thing, action, or idea.

    Example:

    "Maria is reading a book."

    Who is reading?

    Maria.

    What is Maria reading?

    A book.
  `,

  explainAgain: `
    Use this simple trick:

    WHO = person

    WHAT = thing or action

    If the question asks "Who?", look for the person.

    If the question asks "What?", look for the thing or action being discussed.
  `,

  examples: [
    '"John plays basketball." — Who plays? <strong>John.</strong>',
    '"Anna bought a pencil." — What did Anna buy? <strong>A pencil.</strong>',
    '"The teacher opened the door." — Who opened it? <strong>The teacher.</strong>',
    '"Ben ate an apple." — What did Ben eat? <strong>An apple.</strong>'
  ],

  questions: [
    {
      question: '"Maria walks to school." Who walks to school?',
      options: ["school", "Maria", "walks", "nobody"],
      answer: 1,
      explanation: "Maria is the person performing the action."
    },
    {
      question: '"Leo bought a book." What did Leo buy?',
      options: ["Leo", "bought", "book", "nothing"],
      answer: 2,
      explanation: "The sentence tells us that Leo bought a book."
    },
    {
      question: '"The teacher helps Ana." Who helps Ana?',
      options: ["Ana", "teacher", "helps", "school"],
      answer: 1,
      explanation: "The teacher is the person doing the helping."
    },
    {
      question: '"Carlo drinks water." What does Carlo drink?',
      options: ["Carlo", "water", "drinks", "cup"],
      answer: 1,
      explanation: "Water is what Carlo drinks."
    },
    {
      question: '"Mother cooks dinner." Who cooks dinner?',
      options: ["dinner", "mother", "cooks", "father"],
      answer: 1,
      explanation: "Mother is the person doing the action."
    }
  ]
},

{
  id: 7,
  icon: "📍",
  title: "Where",
  subtitle: "Learn how to understand questions about places.",
  goal: "Find where an event or action happens.",

  explanation: `
    WHERE questions ask about a place.

    Example:

    "Anna studies in the library."

    Where does Anna study?

    In the library.

    When you see the word "where," look for the place.
  `,

  explainAgain: `
    WHERE means:

    "At what place?"

    If someone asks:

    "Where is Ben?"

    they want to know Ben's location.

    Look for words such as:

    school

    home

    park

    library

    market

    classroom
  `,

  examples: [
    '"The children play in the park." — Where? <strong>In the park.</strong>',
    '"Dad is in the kitchen." — Where? <strong>In the kitchen.</strong>',
    '"Maria studies at school." — Where? <strong>At school.</strong>',
    '"The cat sleeps under the table." — Where? <strong>Under the table.</strong>'
  ],

  questions: [
    {
      question: '"Ben plays basketball at school." Where does Ben play?',
      options: ["basketball", "Ben", "school", "plays"],
      answer: 2,
      explanation: "School is the place where Ben plays."
    },
    {
      question: '"Mother cooks in the kitchen." Where does Mother cook?',
      options: ["mother", "kitchen", "cooks", "food"],
      answer: 1,
      explanation: "The sentence tells us she cooks in the kitchen."
    },
    {
      question: '"The children are at the park." Where are the children?',
      options: ["school", "home", "park", "store"],
      answer: 2,
      explanation: "They are at the park."
    },
    {
      question: "Which question asks about a place?",
      options: ["Who is she?", "What is that?", "Where is the library?", "When is lunch?"],
      answer: 2,
      explanation: '"Where is the library?" asks for a location.'
    },
    {
      question: '"The book is on the table." Where is the book?',
      options: ["under the chair", "on the table", "inside the bag", "at school"],
      answer: 1,
      explanation: "The sentence clearly says the book is on the table."
    }
  ]
},

{
  id: 8,
  icon: "⏰",
  title: "When",
  subtitle: "Learn words that tell us when something happens.",
  goal: "Recognize basic time words and answer WHEN questions.",

  explanation: `
    WHEN questions ask about time.

    The answer might be:

    today

    tomorrow

    yesterday

    morning

    afternoon

    evening

    night

    Monday

    8:00 AM

    Example:

    "The class starts at 8:00 AM."

    When does the class start?

    At 8:00 AM.
  `,

  explainAgain: `
    WHERE asks about a place.

    WHEN asks about time.

    If someone asks:

    "When will you go?"

    they want to know the time or day.
  `,

  examples: [
    '"I eat breakfast in the <strong>morning</strong>."',
    '"We have class on <strong>Monday</strong>."',
    '"She visited yesterday." — When? <strong>Yesterday.</strong>',
    '"The movie starts at <strong>7:00 PM</strong>."'
  ],

  questions: [
    {
      question: '"We go to school on Monday." When do we go to school?',
      options: ["school", "Monday", "we", "go"],
      answer: 1,
      explanation: "Monday tells us when the action happens."
    },
    {
      question: '"I eat breakfast in the morning." When do I eat breakfast?',
      options: ["morning", "breakfast", "home", "eat"],
      answer: 0,
      explanation: "Morning tells us the time of day."
    },
    {
      question: "Which word tells us about time?",
      options: ["park", "tomorrow", "teacher", "apple"],
      answer: 1,
      explanation: '"Tomorrow" refers to a time.'
    },
    {
      question: '"The game starts at 3:00 PM." When does the game start?',
      options: ["game", "3:00 PM", "starts", "school"],
      answer: 1,
      explanation: "3:00 PM is the time when the game starts."
    },
    {
      question: "Which question asks about time?",
      options: ["Who is your teacher?", "What is that?", "Where is your bag?", "When is your birthday?"],
      answer: 3,
      explanation: '"When is your birthday?" asks about time or date.'
    }
  ]
},

{
  id: 9,
  icon: "❓",
  title: "Question Words",
  subtitle: "Understand the basic meaning of who, what, where, and when.",
  goal: "Choose the correct question word for simple situations.",

  explanation: `
    Question words help us know what information someone wants.

    WHO asks about a person.

    WHAT asks about a thing, action, or idea.

    WHERE asks about a place.

    WHEN asks about time.

    Understanding these four words will make reading questions much easier.
  `,

  explainAgain: `
    Remember this simple guide:

    WHO = person

    WHAT = thing or action

    WHERE = place

    WHEN = time

    Before answering a question, first look at the question word.
  `,

  examples: [
    "<strong>Who</strong> is your teacher? — asks for a person",
    "<strong>What</strong> are you eating? — asks for a thing",
    "<strong>Where</strong> do you live? — asks for a place",
    "<strong>When</strong> does class begin? — asks for a time"
  ],

  questions: [
    {
      question: "_____ is your teacher?",
      options: ["Who", "What", "Where", "When"],
      answer: 0,
      explanation: "The question asks about a person, so we use WHO."
    },
    {
      question: "_____ is your bag?",
      options: ["Who", "What", "Where", "When"],
      answer: 2,
      explanation: "The question asks for the location of the bag, so we use WHERE."
    },
    {
      question: "_____ time does class start?",
      options: ["Who", "What", "Where", "When"],
      answer: 1,
      explanation: '"What time" is used when asking for a specific time.'
    },
    {
      question: "_____ is your birthday?",
      options: ["Who", "Where", "When", "What place"],
      answer: 2,
      explanation: "A birthday has a date, so the question is asking about time."
    },
    {
      question: "_____ are you holding?",
      options: ["What", "When", "Who", "Where"],
      answer: 0,
      explanation: "The question asks about the thing being held, so we use WHAT."
    }
  ]
},

{
  id: 10,
  icon: "🏆",
  title: "Foundation Review",
  subtitle: "Review the basic English ideas from Lessons 1–9.",
  goal: "Show that you understand the main ideas from the Foundation level.",

  explanation: `
    You have learned several important English foundations.

    You learned about:

    naming words

    action words

    describing words

    simple sentences

    who

    what

    where

    when

    This lesson helps you check which ideas you already understand well
    and which ones may need more practice.
  `,

  explainAgain: `
    This is a review lesson.

    Do not worry if you make mistakes.

    Mistakes help us discover what we need to practice.

    Read each question carefully.

    Think about what the question is asking before choosing an answer.
  `,

  examples: [
    "<strong>Naming word:</strong> teacher",
    "<strong>Action word:</strong> run",
    "<strong>Describing word:</strong> happy",
    "<strong>Where:</strong> asks about a place",
    "<strong>When:</strong> asks about time"
  ],

  questions: [
    {
      question: 'What is the naming word in "The dog runs"?',
      options: ["dog", "runs", "the", "fast"],
      answer: 0,
      explanation: "Dog names an animal."
    },
    {
      question: 'What is the action word in "Maria reads a book"?',
      options: ["Maria", "book", "reads", "a"],
      answer: 2,
      explanation: "Reads tells us what Maria is doing."
    },
    {
      question: 'What is the describing word in "The small cat sleeps"?',
      options: ["cat", "small", "sleeps", "the"],
      answer: 1,
      explanation: "Small tells us more about the cat."
    },
    {
      question: '"Anna studies at school." Where does Anna study?',
      options: ["Anna", "studies", "school", "today"],
      answer: 2,
      explanation: "School is the place where Anna studies."
    },
    {
      question: '"The class starts at 8:00 AM." When does class start?',
      options: ["class", "school", "8:00 AM", "teacher"],
      answer: 2,
      explanation: "8:00 AM tells us the time."
    },
    {
      question: "Which is a complete sentence?",
      options: ["The happy", "The student reads.", "Inside the room", "Very slowly"],
      answer: 1,
      explanation: '"The student reads." gives us a complete idea.'
    },
    {
      question: "Which question asks about a person?",
      options: ["Where are you?", "When is lunch?", "Who is your teacher?", "What is that?"],
      answer: 2,
      explanation: "WHO asks about a person."
    },
    {
      question: "Which question asks about a place?",
      options: ["Who called?", "Where is the library?", "When will you go?", "What are you reading?"],
      answer: 1,
      explanation: "WHERE asks about a place."
    },
    {
      question: "Which group contains only action words?",
      options: ["run, read, eat", "teacher, dog, school", "red, happy, big", "morning, Monday, tomorrow"],
      answer: 0,
      explanation: "Run, read, and eat are all actions."
    },
    {
      question: "Which group contains only describing words?",
      options: ["run, walk, read", "big, happy, red", "school, teacher, book", "today, tomorrow, Monday"],
      answer: 1,
      explanation: "Big, happy, and red all describe people or things."
    }
  ]
}

];

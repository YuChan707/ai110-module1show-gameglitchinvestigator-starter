# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The program did not run properly based of the dificulties
- 1- "Game over" button doesn't work
  2- "Go LOWER"/"Go HIGHER" accuracy 

---

## 2. How did you use AI as a teammate?

- Claude
- Mathematical operation for the score, it help me identify where come from the session_state.score. The based (no what I changed) only show the update_score which take different values togather and messed up. I set the rule that only subtract x (the reminder of 100 divided by attempt limit) with the actual score from the sessionn_state
- Use exception cases, for the 0 value

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
First I try understand the variable or function behind or ask claude to deeply explain. Dig in inside and write in the notepad

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
Looking for the left attempt values. It should subtract until get 0 for the 'game over'

- Did AI help you design or understand any tests? How?
 Yes, in the chat demonstrate how it work in the process. What value has variable inside of each action. Step by step. And easy to discuss some missunderstand area.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
activate the terminal (venv). It open e local side of my computer and run. the entire program.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Rerun is like a reset function. When you apply to a function using for a buttom. it re run entire program

- What change did you make that finally gave the game a stable secret number?
I decide to keep it random for each round. It's a game design to take guess number. While it's unpredictable or just by luck. It's more funny

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Anotate the note of the AI, I can lose the chat. So I create a doc file and the explanations. Diging what the AI said, my institives/knowleged and notes

- This could be a testing habit, a prompting strategy, or a way you used Git.
Find descriotion of the enviroment (variable, function or operation) and   de error/bug/problem (my self). Later request the AI, comparing my understand and analized the output

- What is one thing you would do differently next time you work with AI on a coding task?
spend 30 minutes analizing and later discuss with the AI

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Error happens to everybody (human/AI/machine). But recognized is better that denying.


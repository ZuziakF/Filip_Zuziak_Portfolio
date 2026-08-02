# Hi, I'm Filip Zuziak
**Developer | Data Analyst**

Welcome to my portfolio! This repository showcases my diverse programming projects, demonstrating my skills across multiple technologies. My work ranges from designing software architecture and building UI to developing custom machine learning models and performing exploratory data analysis.

### Tech Stack & Core Skills
* **Languages:** Python, C#, C++, R
* **Technologies & Frameworks:** WPF, .Net, NumPy, Scikit-Learn, Raylib, Pandas 
* **Key Competencies:** Object-Oriented Programming, Web Development, Machine Learning, Data Visualization, Data Analysis

---

## Featured Projects

### [XAU/USD Market Prediction: Custom Neural Networks & Classic ML](<./Custom Neural Networks & Classic ML>)
A comprehensive machine learning project focused on predicting gold market prices and trend directions. The primary objective was a deep exploration of ML algorithms by building a Multi-Layer Perceptron.
* **Tech Stack:** `Python`, `NumPy`, `Scikit-Learn`
* A neural network built directly on NumPy matrices, covering the forward pass, backpropagation, and weight updates, with a choice of sigmoid, ReLU, or tanh activations. Trained on gold XAU/USD data for two tasks: regression, which predicts the next-day price, and classification, which predicts direction, whether the price goes up or down.

The script tests one parameter at a time around a fixed baseline configuration, including `neuron count`, `learning rate`, `number of epochs`, `activation function`, `train/test split`, and `number of hidden layers`, to see how each one affects performance.

*Console output shown below: (for the regression task)*

Each table corresponds to one tested parameter, with each row showing a different value tried. The network is trained five times per value, since weights start randomly, and the columns report the average and best error on both the training set and the test set. `Błąd TRAIN` reflects how well the network fits data it has already seen, while `Błąd TEST` reflects performance on unseen data, which is the more meaningful measure of real-world accuracy. Both errors are mean squared error computed on the standardized target, meaning the price is scaled to zero mean and unit variance before the error is calculated, so the values reflect relative deviation rather than dollar amounts.

> **Model Training Results (Regression Analysis):**
> ![ML Console Output](./images/regression.png)

Second part swaps in scikit-learn's built-in models on the same regression and classification setup, to compare against tuned, ready-made implementations. Each method has its own core parameter being tested: `number of neighbors` for **kNN**, `maximum tree depth` for **Decision Tree**, `number of trees` for **Random Forest**, and the `regularization strength C` for **SVM**.

*Console output shown below:*

The `Regresja MSE` column reports mean squared error for the regression task, with RMSE shown in parentheses since it's in the same units as the price and easier to interpret directly. The `Klasyfikacja` column reports classification accuracy, the percentage of correctly predicted price directions.

> **Model Training Results (scikit-learn):**
> 
> ![ML Console Output](./images/um.png)

### [Athlete Management System](<./Athlete Management System>)
A multi-layered desktop application designed for managing winter sports athletes, highlighting a professional approach to software engineering and robust architecture.
* **Tech Stack:** `C#`, `WPF`, `.NET`

A desktop application for organizations running winter sports competitions, built to handle athletes, clubs, and competition results in one place. Admins log in through a dedicated authentication system and manage everything from there.

The system covers the full structure of running a competition. Admins can create competitions, register athletes, and set up clubs, then assign athletes to the clubs they belong to. Each club has its own entry requirements, including a minimum point threshold an athlete needs to join, a maximum age limit, and a cap on how many athletes it can hold. Competitions have their own settings too, with a difficulty level on a scale from one to five and a points system based on final placement.

Once a competition takes place, admins record each athlete's result, which feeds back into their overall point total and determines whether they meet the requirements for higher level clubs.

> **Application Interface (Main Dashboard & Login):**
> ![Athlete System GUI](./images/gui.png)
> ![Athlete System Login](./images/login.png)

---

## Data Analysis & Utilities

### [Exploratory Data Analysis (EDA)](<./EDA Analysis>)
An Exploratory Data Analysis project focused on statistical data processing and insights generation.
* **Tech Stack:** `R`, `ggplot2`, `tidyverse`

An exploratory analysis of a dataset on social media addiction among students, covering habits, demographics, and wellbeing across roughly seven hundred respondents aged 16 to 25. The dataset includes variables such as `daily usage hours`, `sleep patterns`, `mental health scores`, `academic performance`, and `relationship status`, alongside an overall `addiction score`.

The analysis moves from data cleaning and handling missing values into exploring how these variables relate to each other, backed by correlation matrices, chi-squared tests, and t-tests rather than just visual impressions. The strongest signal in the whole dataset turned out to be mental health, which correlated at minus 0.95 with the addiction score, meaning addiction and mental wellbeing move almost in lockstep in opposite directions. Sleep followed a similar pattern, and students involved in more conflicts over social media were consistently more likely to report it hurting their academic performance. Gender, on the other hand, showed no meaningful effect on addiction levels once tested statistically.


### [Lorenz Curve & Gini Coefficient Calculator](<./Lorenz Curve>)
A Python utility application that automates economic data analysis based on spreadsheet inputs.
* **Tech Stack:** `Python`, `GUI Library`, `Pandas / Openpyxl`

A small desktop tool for measuring income inequality from spreadsheet data. The user picks an Excel file through a simple tkinter interface, and the app reads the income column, calculates the Gini coefficient, and plots the Lorenz curve alongside the line of perfect equality for comparison.

The Gini coefficient is computed directly from the formula rather than through a statistics library, and the Lorenz curve is built from cumulative income shares plotted against cumulative population share. Errors like a missing file or a missing income column are caught and shown to the user instead of crashing the app.


---

##  Game Development

###  [Tetris](./Tetris)
* **Tech Stack:** `C++`, `Raylib`

A classic Tetris implementation split into clear, separate modules instead of one large file. Grid logic, block shapes, positioning, color handling, and the main game loop each live in their own header and source files, which keeps the codebase easy to navigate and each piece testable on its own.

The project handles the core Tetris mechanics: falling blocks, rotation, collision with the grid and other blocks, line clearing, and game state, built around a coordinate and grid system that tracks where each block currently sits on the board.

Built following a YouTube tutorial as a way to learn modular project structure and more advanced game state management.

###  [Pong Game](<./Pong>)
* **Tech Stack:** `C++`, `Raylib`

A classic Pong clone built to practice object-oriented structure in a real-time game loop. The ball, player paddle, and CPU paddle are each their own class, with a shared base Paddle class handling movement and screen boundaries, and a CPUPaddle subclass adding simple AI that tracks the ball's vertical position.

Collision detection is handled per frame between the ball and both paddles, reversing the ball's direction on contact, while hitting either side wall scores a point and resets the ball to the center with a randomized direction. The game keeps score for both sides and displays it live on screen.

Built following a YouTube tutorial to learn game loop structure, collision handling, and OOP patterns in C++.

### [Snake Game](<./Snake Game>)
* **Tech Stack:** `Python`, `turtle`

A Snake implementation built with Python's turtle graphics library. The snake grows one segment each time it eats, with each body part following the position of the one ahead of it in the previous frame, which is what keeps the trail moving smoothly behind the head.

Hitting the screen border or colliding with its own body resets the game, sending the body segments off screen, clearing the score, and restoring the starting speed. Eating food also gradually speeds up the game by shortening the delay between frames, making it harder to control the longer the snake gets. A live scoreboard tracks both the current score and the high score across resets.

Built following a YouTube tutorial to practice core game logic and event handling.

# Introduction
This is a chemistry balancing application supporting both plain text and "Periodic Table Keyboard" input. Balancing algorithms available to select include 1. Tree search (brute force) and 2. Gaussian elimination (standard, Recommended).

# Application setup and launching
1. Prepare your Python environment. Flask is required.
2. Clone code to your local repository.
3. Run app.py and launch the application on localhost:5007 on a web browser.

# Input methods and result display
1. Write chemestry equations with no coefficients, separated by '+' and '=', in the top box and click "Fill inputbox". Then, the left and right hand side of the equation will be displayed in the below two boxes.
2. Alternatively, use the virtual periodic-table-keyboard to type equation directly in the 2 input boxes, switching to left and right with the arrow keys.
3. Choose a balancing algorithm and click the corresponding button to see result. 
4. For tree search algorithm, all trials of coefficients will be displayed.
5. For gaussian elimination algorithm, the formation of linear equations and matrix calculation results will be displayed. 

# Future improvement plan (according to user suggestions)
1. Include subscript display to approximate real chemistry expressions.
2. Check matrix rank of gaussian elimination to detect multiple or no solution scenarioss.
3. Allow merged input of compounds like CuSO4'5H2O as a whole term.
4. Improve combined virtual keyboard input and physical keyboard typing, solving some misleading bugs.

# New features
Python code editor similar to virtual chemistry keyboard. To be developed.
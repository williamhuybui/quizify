# Quizify

Quizify is a web application built using Dash that leverages the OpenAI API to translate text inputs into multiple-choice questions. With Quizify, you can easily convert paragraphs, articles, or any other text into interactive quizzes, making it a valuable tool for educators, content creators, and anyone looking to engage their audience through interactive learning experiences.

## Features

- **Text-to-Question Translation**: Quizify utilizes the power of the OpenAI API to automatically generate multiple-choice questions from text inputs. Simply provide your text, and Quizify will transform it into a quiz format, complete with answer options.
- **Customizable Quiz Parameters**: Quizify allows you to fine-tune various parameters of your quizzes, such as the number of questions, difficulty level, and more. Tailor your quizzes to suit your specific needs and audience.
- **Interactive User Interface**: The user interface of Quizify is intuitive and user-friendly, providing a seamless experience for both quiz creators and quiz takers.
- **Real-time Feedback**: Quizify provides instant feedback to quiz takers, allowing them to see their progress and results immediately after completing a quiz.
- **Quiz History**: Quizify keeps track of the quizzes you have created, allowing you to access and review them at any time.

## Installation

To run Quizify locally, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/williamhuybui/quizify.git
   ```

2. Navigate to the project directory:

   ```
   cd quizify
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Obtain an OpenAI API key by following the instructions in the [OpenAI API documentation](https://platform.openai.com/docs/authentication).

5. Set the API key as an environment variable. You can either export it in your terminal session or store it in a `.env` file in the project root directory:

   ```
   export OPENAI_API_KEY=<your-api-key>
   ```

   or

   ```
   OPENAI_API_KEY=<your-api-key>
   ```

6. Run the application:

   ```
   python main.py
   ```

7. Access Quizify in your web browser at `http://localhost:8050`.

## Usage

1. Enter the text you want to convert into a quiz in the provided input field.
2. Adjust the quiz parameters, such as the number of questions  as desired.
3. Click the "Generate Quiz" button.
4. Quizify will process the text and generate multiple-choice questions based on the input.
5. Share the generated quiz with others by providing them with the generated link.
6. Quiz takers can access the quiz through the provided link, answer the questions, and receive real-time feedback.

## Contributing

Contributions to Quizify are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/williamhuybui/quizify.git). If you would like to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your branch to your forked repository.
5. Submit a pull request to the `main` branch of the original repository.

Please ensure that your code adheres to the existing coding style and is well-documented.

## License

Quizify is released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this application as per the terms of the license.

## Acknowledgements

- This application was built using the [Dash](https://dash.plotly.com/) framework.
- Quizify utilizes the power of the [OpenAI API](https://platform.openai.com/) for text-to-question translation.

## Contact

If you have any questions or feedback, feel free to reach out:

- Email: [williamhuybui@gmail.com](mailto:williamhuybui@gmail.com)

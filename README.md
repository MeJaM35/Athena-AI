# Athena AI

Athena AI is a comprehensive branding and marketing solution that helps businesses with 100% of their written and voice branding, and 80% of their marketing efforts. It covers everything a company needs from a branding and marketing perspective, leaving only paid media management and similar aspects to be handled externally.

## Features
- Complete written and voice branding solutions.
- Marketing tools for 80% of marketing needs.
- Easy integration with existing systems for managing and building brands.

## Setup

### Prerequisites
- Ensure that you have Python installed. Check the version using the command:

```bash
python --version
```

### API Credentials Setup
Before running the application, you need to set up the following credentials:

1. **Google OAuth Credentials**:
   - Go to the Google Cloud Console
   - Create a new project or select an existing one
   - Enable the OAuth 2.0 API
   - Create OAuth 2.0 credentials
   - Add your credentials to `.env` file:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```

2. **OpenAI API Key**:
   - Sign up for an OpenAI account
   - Generate an API key from your OpenAI dashboard
   - Add your OpenAI key to `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### Install Dependencies
Install the required dependencies for the Django project:

```bash
pip install -r requirements.txt
```

### Database Migrations
Make and apply migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server
To start the development server, run:

```bash
python manage.py runserver
```

## Contributing
If you'd like to contribute to the development of this project, feel free to fork the repository, submit a pull request, or open an issue. All contributions are welcome!

## License
This project is licensed under the MIT License.

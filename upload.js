// upload.js (Netlify function)
const { IncomingForm } = require('formidable');
const fs = require('fs');

exports.handler = async (event, context) => {
  return new Promise((resolve, reject) => {
    const form = new IncomingForm();
    form.parse(event, (err, fields, files) => {
      if (err) {
        return resolve({
          statusCode: 500,
          body: JSON.stringify({ error: 'Error parsing the files.' }),
        });
      }

      // Save the uploaded files to a directory or GitHub repo
      // This is a placeholder. Implement GitHub upload here if needed.

      resolve({
        statusCode: 200,
        body: JSON.stringify({
          message: 'Files uploaded successfully',
          files: Object.values(files).map(file => ({
            name: file.name,
            path: file.path,
          })),
        }),
      });
    });
  });
};

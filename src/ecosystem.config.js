module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "gunicorn",
      args: "-w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000",
      interpreter: "python3",
    },
  ],
};

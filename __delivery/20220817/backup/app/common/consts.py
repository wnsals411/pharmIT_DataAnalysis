JWT_SECRET = "PHARM1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", '/login/',"/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth|/static/|/api/login/)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins

FROM python:3.9.5


# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/ds_project_api

ARG PIP_EXTRA_INDEX_URL

# Install requirements, including from Gemfury
ADD ./ds_project_api /opt/ds_project_api/
RUN pip install --upgrade pip
RUN pip install -r /opt/ds_project_api/requirements_api/requirements.txt

RUN chmod +x /opt/ds_project_api/run.sh
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

EXPOSE 8001

CMD ["bash", "./run.sh"]

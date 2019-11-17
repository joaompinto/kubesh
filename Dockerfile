FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip3 install /app
CMD ["kubesh"]
ENV KUBECONFIG=/app/kube_config
# USER 1001

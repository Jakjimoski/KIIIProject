## Опис
ова е проектна задача по предметот КИИИ и е едноставна веб апликација за управување со книги. 
Апликацијата овозможува додавање, уредување и бришење на книги, како и додавање автори и жанрови. 
Дополнително, системот пресметува статистики како просечна оцена, број на книги и најново додадена книга.

## Технологии
-**Backend**: Django
-**Frontend**: Streamlit
-**База на податоци**: PostgreSQL
-**Инфраструктура**: Docker, Kubernetes (k3d)
-**Верзионирање**: GitHub

### 1. Креирај кластер со k3d
```bash
k3d cluster create library-cluster

Примени ги манифестите во овој редослед

kubectl apply -f namespace.yaml
kubectl apply -f postgres.yaml -n library-namespace
kubectl apply -f backend.yaml -n library-namespace
kubectl apply -f frontend.yaml -n library-namespace
kubectl apply -f ingress.yaml -n library-namespace

Провери состојба

kubectl get all -n library-namespace

Port-froward за Streamlit

kubectl port-forward -n library-namespace deployment/streamlit-frontend 8501:8501

За пристап, во прелистувач навигирај до: http://localhost:8501



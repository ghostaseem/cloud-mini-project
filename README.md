Rest Application
=================

This is Flask and Cassandra RESTful application.
It has feature like:
1.  Hash based user authentication.
2.  Dynamically generated REST API.
3.  API for Weather (api.apixu.com) and Location by IP (api.ipgeolocation.io) has been used.

Installation
------------

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

Running
-------

To run the server use the following command:

    (venv) $ python app.py
     * Running on http://0.0.0.0:8080/
     * Restarting with reloader

Then from a different terminal window you can send requests.

Further Implementation
-----------------------
You can you HTTPS if you are deploying it on specific domain.
You cannot use HTTPS in bare IP.

If you are deploying using kubernetes here is the code:

    $ curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh
    $ chmod 700 get_helm.sh
    $ ./get_helm.sh


    helm init


    kubectl create serviceaccount tiller --namespace kube-system

    kubectl create clusterrolebinding tiller-cluster-rule \
    --clusterrole=cluster-admin \
    --serviceaccount=kube-system:tiller


    helm init --service-account=tiller

    kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}' 
 
    helm install --name cert-manager \
    --namespace ingress \
    --set ingressShim.defaultIssuerName=letsencrypt-prod \
    --set ingressShim.defaultIssuerKind=ClusterIssuer \
    stable/cert-manager \
    --version v0.5.2


    kubectl get crd


    cat << EOF| kubectl create -n ingress -f -
    apiVersion: certmanager.k8s.io/v1alpha1
    kind: ClusterIssuer
    metadata:
    name: letsencrypt-prod
    spec:
    acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: aseempok@gmail.com
    privateKeySecretRef:
    name: letsencrypt-prod
    http01: {}
    EOF



    cat > values.yaml <<EOF
    serviceType: ClusterIP
    ghostHost: {Your domain name}
    ingress:
    enabled: true
    hosts:
    - name: {Your domain name}
      tls: true
      tlsSecret: test-app-tls
      annotations:
        kubernetes.io/ingress.class: nginx
        kubernetes.io/tls-acme: "true"
    mariadb:
    replication:
    enabled: true
    EOF

    helm install --name test-app \
    -f values.yaml \
    stable/ghost



Project Documentation
-----------------------

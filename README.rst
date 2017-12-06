===============================
PyData Zurich meetup Blockchain
===============================

This is a basic implementation of the **Build your own Blockchain** 🎄 PyData Zurich 🎄 Xmas special.

The app is deployed on Heroku an accessible `here <https://blockchain-pydatazrh.herokuapp.com/#/default`_.

The code is mainly derived from this `repository <https://github.com/dvf/blockchain>`_.


To run the blockchain in a docker environment run::

    > docker build -t blockchain_pydatazrh:latest .


    > docker run -d -p 8080:5000 blockchain_pydatazrh



If you want to run it on your own Heroku account simply type::

    > heroku login

    > heroku create

    > git push heroku master

    > heroku ps:scale web=1

    > heroku open
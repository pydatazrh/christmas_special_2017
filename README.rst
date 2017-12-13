===============================
PyData Zurich meetup Blockchain
===============================

This is a basic implementation of the **Build your own Blockchain** 🎄 PyData Zurich 🎄 Xmas special.

The code is mainly derived from this `repository <https://github.com/dvf/blockchain>`_.

Click the badge to run the notebooks from your browser:

.. image:: https://mybinder.org/badge.svg
  :target: https://mybinder.org/v2/gh/pydatazrh/christmas_special_2017/master?filepath=notebooks

The app is deployed on Heroku an accessible `here <https://blockchain-pydatazrh.herokuapp.com/#/default>`_ .


To run the application locally make sure to have all dependencies installed and then launch the server::

    > pip3 install -r requirements.txt

    > python3 api.py


To run the blockchain in a docker environment run::

    > docker build -t blockchain_pydatazrh:latest .


    > docker run -d -p 8080:5000 blockchain_pydatazrh



If you want to run it on your own Heroku account simply type::

    > heroku login

    > heroku create

    > git push heroku master

    > heroku ps:scale web=1

    > heroku open

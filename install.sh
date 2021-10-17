docker image build -t xi_bot .

echo Build successfully

docker run -d --name xi_bot xi_bot

echo Added container
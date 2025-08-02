cd ..
poetry remove arpakitlib
echo "yes" | poetry cache clear --all PyPI
echo "yes" | poetry cache clear --all pypi
echo "yes" | poetry cache clear --all testpypi
poetry add arpakitlib
poetry lock
for /r %%f in (gists_files\*) do (
	cloc.exe %%f --out="test\%%~nxf.csv" --csv
)
<h1>Basket – Fizička simulacija</h1>
<h2>Kratak Opis Problema</h2>
2D simulacija koja se sastoji od terena, koša, i košarkaških lopti. Igraču će biti omogućeno pomeranje i kontrolisanje lopte koristeći miš. Igrica nema unapred definisana pravila, već je na igraču da odluči šta će da radi; Da pokuša da ubaci loptu u koš iz daleka, ili da se igra sa podešavanjima i gleda kako to utiče na fiziku. Svaki put kad je lopta ubačena u koš, brojač se poveća, pa igrač tako može voditi računa o svojim poenima.
<h2>Detaljnija specifikacija</h2>
<h3>Kinematika</h3>
<h4>Linearno kretanje</h4>
Na loptu uticaće gravitacija, kao i vetar ukoliko je uključen u podešavanjima. Na loptu će takođe uticati sila dok je igrač vuče kursorom. 
<h4>Rotaciono kretanje</h4>
Kako na loptu utiče sila, i kako odskače od zemlje, doći će i do rotacije koja će biti uračunata.
Kretanje rešavaće se Ojlerovom metodom.
<h3>Detekcija kolizija</h3>
<h4>Krug na duž</h4>
Detekcija kolizije krug na duž dešavaće se kada je lopta uspešno ubačena u koš, i tada će doći do povećanja brojača za poene. Takođe će do kolizije doći kada lopta pogodi ivice ekrana ili tlo.
<h4>Krug na krug</h4>
Detekcija kolizije krug na krug desiće se ako igrač odluči da igra sa više od jedne lopte i dođe do kolizija između lopti. 
<h4>Krug na poligon</h4>
Detekcija kolizije krug na poligon desiće se prilikom sudara lopte u košarkašku tablu ili obruč.<br><br>
<p>Za detekciju kolizije koristiće se Separating Axis Test (SAT)</p>
<h3>Ograničeno kretanje</h3>
<h4>Rezultat kontakata</h4>
Kretanje lopte je ograničeno kontaktima kada se lopta kotrlja po terenu, i u svakom trenutku biće uračunata sila trenja pri kotrljanju.
<h4>Unapred definisano</h4>
Obruč koša neće biti fiksiran u mestu, već će inercija lopte uticati na njega pri sudaru, i biće kao zglob koji je u tački vezan za košarkašku tablu.<br><br>
<p>Grafički prikaz biće implementiran pomoću pygame biblioteke za python programski jezik.</p>
<h3>Podela Rada</h3>
<p>Miloš Milić (SV10/2022) biće zadužen za implementaciju kinematike i detekcije kolizija.</p>
<p>Mirko Đukić (SV32/2022) biće zadužen za implementaciju kontakata pri ograničenom kretanju i unapred definisano ograničeno kretanje.</p>
<p>Interfejs i grafički prikaz će biti zajednički implementiran.</p>
Literatura
Kolizije u igrama: https://studiofreya.com/3d-math-and-physics/collision-detection-in-practice/ <br>
Kinematika u igrama: http://www.toptal.com/game/video-game-physics-part-i-an-introduction-to-rigid-body-dynamics <br>
Kolizija kruga: https://www.jeffreythompson.org/collision-detection/poly-circle.php <br>
Rešavanje kolizija u igrama: https://www.chrishecker.com/images/e/e7/Gdmphys3.pdf <br>
Ograničeno kretanje u igrama: https://www.toptal.com/game/video-game-physics-part-iii-constrained-rigid-body-simulation <br>
Rad sa pygame bibliotekom: https://www.pygame.org/wiki/tutorials <br>
